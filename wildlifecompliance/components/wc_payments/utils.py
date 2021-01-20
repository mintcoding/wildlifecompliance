# from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
# from django.conf import settings
# from django.core.exceptions import ValidationError
# from django.db import transaction

from datetime import datetime, timedelta, date
# from dateutil.relativedelta import relativedelta
# from commercialoperator.components.main.models import Park
# from commercialoperator.components.proposals.models import Proposal
# from commercialoperator.components.organisations.models import Organisation
# from commercialoperator.components.bookings.models import Booking, ParkBooking, BookingInvoice, ApplicationFee
# from commercialoperator.components.bookings.email import send_monthly_invoice_tclass_email_notification
# from ledger.checkout.utils import create_basket_session, create_checkout_session, calculate_excl_gst
from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.db.models.signals import post_save
from django.http.response import HttpResponseRedirect
from django.urls import reverse

from ledger.checkout.utils import create_basket_session, create_checkout_session
from ledger.payments.bpoint.models import BpointTransaction
from ledger.payments.cash.models import CashTransaction
from ledger.payments.models import Invoice
# from ledger.payments.utils import oracle_parser
# import json
# import ast
from decimal import Decimal

import logging

from oscar.apps.order.models import Order

from wildlifecompliance import settings
from wildlifecompliance.components.sanction_outcome.models import SanctionOutcome, SanctionOutcomeUserAction
from wildlifecompliance.components.wc_payments.models import InfringementPenalty, InfringementPenaltyInvoice

logger = logging.getLogger('payment_checkout')


def get_session_infringement_invoice(session):
    """ Infringement Penalty session ID """
    if 'wc_infringement_invoice' in session:
        wc_infringement_id = session['wc_infringement_invoice']
    else:
        raise Exception('Infringement Penalty not in Session')

    try:
        return InfringementPenalty.objects.get(id=wc_infringement_id)
    except Invoice.DoesNotExist:
        raise Exception('Infringement Penalty not found for Sanction Outcome {}'.format(wc_infringement_id))


def set_session_infringement_invoice(session, infringement_penalty):
    """ Infringement Penalty session ID """
    session['wc_infringement_invoice'] = infringement_penalty.id
    session.modified = True


def delete_session_infringement_invoice(session):
    """ Infringement Penalty session ID """
    if 'wc_infringement_invoice' in session:
        del session['wc_infringement_invoice']
        session.modified = True


def checkout(request, proposal, lines, return_url_ns='public_booking_success', return_preload_url_ns='public_booking_success', invoice_text=None, vouchers=[], internal=False):
    #import ipdb; ipdb.set_trace()
    basket_params = {
        'products': lines,
        'vouchers': vouchers,
        'system': settings.WC_PAYMENT_SYSTEM_ID,
        'custom_basket': True,
    }

    basket, basket_hash = create_basket_session(request, basket_params)
    #fallback_url = request.build_absolute_uri('/')
    checkout_params = {
        'system': settings.WC_PAYMENT_SYSTEM_ID,
        'fallback_url': request.build_absolute_uri('/'),                                      # 'http://mooring-ria-jm.dbca.wa.gov.au/'
        'return_url': request.build_absolute_uri(reverse(return_url_ns)),          # 'http://mooring-ria-jm.dbca.wa.gov.au/success/'
        'return_preload_url': request.build_absolute_uri(reverse(return_url_ns)),  # 'http://mooring-ria-jm.dbca.wa.gov.au/success/'
        'force_redirect': True,
        'proxy': True if internal else False,
        'invoice_text': invoice_text,                                                         # 'Reservation for Jawaid Mushtaq from 2019-05-17 to 2019-05-19 at RIA 005'
    }
    #    if not internal:
    #        checkout_params['check_url'] = request.build_absolute_uri('/api/booking/{}/booking_checkout_status.json'.format(booking.id))
    if internal or request.user.is_anonymous():
        #checkout_params['basket_owner'] = booking.customer.id
        checkout_params['basket_owner'] = proposal.submitter_id


    create_checkout_session(request, checkout_params)

    #    if internal:
    #        response = place_order_submission(request)
    #    else:
    response = HttpResponseRedirect(reverse('checkout:index'))
    # inject the current basket into the redirect response cookies
    # or else, anonymous users will be directionless
    response.set_cookie(
        settings.OSCAR_BASKET_COOKIE_OPEN, basket_hash,
        max_age=settings.OSCAR_BASKET_COOKIE_LIFETIME,
        secure=settings.OSCAR_BASKET_COOKIE_SECURE, httponly=True
    )

    return response


def create_other_invoice(request, sanction_outcome):
    with transaction.atomic():
        try:
            logger.info('Creating OTHER (CASH/CHEQUE) invoice for sanction outcome: {}'.format(sanction_outcome.lodgement_number))
            order = create_invoice(sanction_outcome, payment_method='other')
            invoice = Invoice.objects.get(order_number=order.number)

            # infringement_penalty, created = InfringementPenalty.objects.get_or_create()
            # infringement_penalty.created_by = request.user
            # infringement_penalty.payment_type = InfringementPenalty.PAYMENT_TYPE_RECEPTION
            # infringement_penalty.save()
            sanction_outcome.infringement_penalty.created_by = request.user
            sanction_outcome.infringement_penalty.payment_type = InfringementPenalty.PAYMENT_TYPE_RECEPTION
            sanction_outcome.save()

            infringement_penalty_invoice, created = InfringementPenaltyInvoice.objects.get_or_create(infringement_penalty=sanction_outcome.infringement_penalty,
                                                                                                     invoice_reference=invoice.reference)

            return invoice

            # invoice_ref = invoice.reference
            # fee_inv, created = InfringementPenaltyInvoice.objects.get_or_create(infringement_penalty=infringement_penalty,
            #                                                                     invoice_reference=invoice_ref)
            # return fee_inv

        except Exception as e:
            logger.error('Failed to create OTHER invoice for sanction outcome: {}'.format(sanction_outcome.lodgement_number))
            logger.error('{}'.format(e))


def create_invoice(sanction_outcome, payment_method='bpay'):
    """
    This will create and invoice and order from a basket bypassing the session
    and payment bpoint code constraints.
    """
    from ledger.checkout.utils import createCustomBasket
    from ledger.payments.invoice.utils import CreateInvoiceBasket

    products = sanction_outcome.as_line_items
    user = sanction_outcome.get_offender()[0]
    invoice_text = 'Payment Invoice'

    basket = createCustomBasket(products, user, settings.WC_PAYMENT_SYSTEM_ID)
    order = CreateInvoiceBasket(payment_method=payment_method, system=settings.WC_PAYMENT_SYSTEM_PREFIX).create_invoice_and_order(basket, 0, None, None, user=user, invoice_text=invoice_text)

    return order
