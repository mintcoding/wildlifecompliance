from wsgiref.util import FileWrapper

from django.http import HttpResponse

from wildlifecompliance.components.call_email.models import Location
from wildlifecompliance.components.call_email.serializers import LocationSerializer
from wildlifecompliance.components.main.serializers import (
    TemporaryDocumentCollectionSerializer,
    BookingSettlementReportSerializer, OracleSerializer)
from wildlifecompliance.components.main.models import TemporaryDocumentCollection
from wildlifecompliance.components.main.process_document import save_document, cancel_document, delete_document
from rest_framework import viewsets, serializers, status, generics, views, filters
from rest_framework.decorators import (
    detail_route,
    list_route,
    renderer_classes,
    parser_classes,
    api_view
)

from wildlifecompliance.components.wc_payments import reports
from wildlifecompliance.helpers import is_internal
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.core.exceptions import ValidationError
import traceback
from django.db import transaction
from ledger.payments.utils import oracle_parser

from wildlifecompliance.settings import WC_PAYMENT_SYSTEM_PREFIX, SYSTEM_NAME


def save_location(location_request_data, *args, **kwargs):
    try:
        if location_request_data.get('id'):
            location_instance = Location.objects.get(id=location_request_data.get('id'))
            location_serializer = LocationSerializer(
                instance=location_instance,
                data=location_request_data,
                partial=True
            )
            location_serializer.is_valid(raise_exception=True)
            if location_serializer.is_valid():
                location_serializer.save()
        else:
            location_serializer = LocationSerializer(
                data=location_request_data,
                partial=True
            )
            location_serializer.is_valid(raise_exception=True)
            if location_serializer.is_valid():
                location_instance = location_serializer.save()
        return location_serializer.data
    except serializers.ValidationError:
        print(traceback.print_exc())
        raise
    except ValidationError as e:
        if hasattr(e, 'error_dict'):
            raise serializers.ValidationError(repr(e.error_dict))
        else:
            # raise serializers.ValidationError(repr(e[0].encode('utf-8')))
            raise serializers.ValidationError(repr(e[0]))
    except Exception as e:
        print(traceback.print_exc())
        raise serializers.ValidationError(str(e))


class TemporaryDocumentCollectionViewSet(viewsets.ModelViewSet):
    queryset = TemporaryDocumentCollection.objects.all()
    serializer_class = TemporaryDocumentCollectionSerializer

    def get_queryset(self):
        # import ipdb; ipdb.set_trace()
        #user = self.request.user
        if is_internal(self.request):
            return TemporaryDocumentCollection.objects.all()
        return TemporaryDocumentCollection.objects.none()

    def create(self, request, *args, **kwargs):
        print("create temp doc coll")
        print(request.data)
        try:
            with transaction.atomic():
                serializer = TemporaryDocumentCollectionSerializer(
                        data=request.data, 
                        )
                serializer.is_valid(raise_exception=True)
                if serializer.is_valid():
                    instance = serializer.save()
                    save_document(request, instance, comms_instance=None, document_type=None)

                    return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e, 'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                # raise serializers.ValidationError(repr(e[0].encode('utf-8')))
                raise serializers.ValidationError(repr(e[0]))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST'])
    @renderer_classes((JSONRenderer,))
    # Designed for uploading comms_log files within "create" modals when no parent entity instance yet exists
    # response returned to compliance_file.vue
    def process_temp_comms_log_document(self, request, *args, **kwargs):
        print("process_temp_comms_log_document")
        print(request.data)
        try:
            instance = self.get_object()
            action = request.data.get('action')
            #comms_instance = None

            if action == 'list':
                pass

            elif action == 'delete':
                delete_document(request, instance, comms_instance=None, document_type=None)

            elif action == 'cancel':
                cancel_document(request, instance, comms_instance=None, document_type=None)

            elif action == 'save':
                save_document(request, instance, comms_instance=None, document_type=None)

            returned_file_data = [dict(
                        file=d._file.url,
                        id=d.id,
                        name=d.name,
                        ) for d in instance.documents.all() if d._file]
            return Response({'filedata': returned_file_data})

        except Exception as e:
            print(traceback.print_exc())
            raise e


class BookingSettlementReportView(views.APIView):
    renderer_classes = (JSONRenderer,)

    def get(self,request,format=None):
        try:
            http_status = status.HTTP_200_OK
            #parse and validate data
            report = None
            data = {
                "date":request.GET.get('date'),
            }
            serializer = BookingSettlementReportSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            filename = 'Booking Settlement Report-{}'.format(str(serializer.validated_data['date']))
            # Generate Report
            report = reports.booking_bpoint_settlement_report(serializer.validated_data['date'])
            if report:
                response = HttpResponse(FileWrapper(report), content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
                return response
            else:
                raise serializers.ValidationError('No report was generated.')
        except serializers.ValidationError:
            raise
        except Exception as e:
            traceback.print_exc()


def oracle_integration(date, override):
    system = WC_PAYMENT_SYSTEM_PREFIX
    #oracle_codes = oracle_parser(date, system, 'Commercial Operator Licensing', override=override)
    oracle_codes = oracle_parser(date, system, 'WildlifeCompliance', override=override)


class OracleJob(views.APIView):
    renderer_classes = [JSONRenderer,]
    def get(self, request, format=None):
        try:
            data = {
                "date":request.GET.get("date"),
                "override": request.GET.get("override")
            }
            serializer = OracleSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            oracle_integration(serializer.validated_data['date'].strftime('%Y-%m-%d'),serializer.validated_data['override'])
            data = {'successful':True}
            return Response(data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            raise serializers.ValidationError(repr(e.error_dict)) if hasattr(e, 'error_dict') else serializers.ValidationError(e)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e[0]))
