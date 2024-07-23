from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action, parser_classes
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.message_txt import MessageTxt


class CustomGenericMixin:
    status_code = ''
    message = ''
    result = ''
    order_by = 'id'

    @staticmethod
    def response_json(result, code='', message='', statuscode='', error_message='', count=None):
        response = {
            'code': code,
            'message': message,
            'data': {
                'count': count,
                'next': result.get('next', 0),
                'previous': result.get('previous', 0),
                'last_page': result.get('last_page', 0),
                'page_size': result.get('page_size', 0),
                'current_page_no': result.get('current_page_no', 0),
                'result': result['results'] if result and 'results' in result else {}
            },
        }
        return response

    def finalize_response(self, request, response, *args, **kwargs):
        """ pass the value to response json function"""
        return super().finalize_response(request, response, *args, **kwargs)


class CustomCreateModelMixin(CreateModelMixin):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        return Response({'message': MessageTxt.Success200}, status=status.HTTP_201_CREATED)


class CustomCreateAPIView(CustomCreateModelMixin,
                          GenericAPIView):
    """
    Concrete view for creating a model instance.
    """

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BaseViewSet(CustomGenericMixin):
    pass


class BaseModelViewSetApi(CustomGenericMixin,
                          ModelViewSet):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ('-id',)

    # def partial_update(self, request, *args, **kwargs):
    #     return self.http_method_not_allowed(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if hasattr(instance, 'is_archived'):
            instance.is_archived = True
            instance.save()
        else:
            instance.delete()


class BasePanelModelViewSetApi(ModelViewSet):
    # permission_classes = [IsStaffPermission]
    ordering_fields = ('id',)

    def perform_destroy(self, instance):
        if hasattr(instance, 'is_archived'):
            instance.is_archived = True
            instance.save()
        else:
            instance.delete()


class ListItemsAPIView(ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = None


class FileUploadingMixin:
    """
    Mixin for uploading files. Change parser to MultiPartParser to allow file uploads for upload_file action

    """

    @action(methods=['POST', ], detail=False, url_name='upload')
    @parser_classes([MultiPartParser, FormParser])
    def upload(self, request, *args, **kwargs):
        with transaction.atomic():
            file_serializer = self.get_serializer(data=request.data)
            if file_serializer.is_valid():
                file_serializer.save()
                return Response(file_serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise Exception(file_serializer.errors)


class PaginationInActionMixin:
    """
    Mixin for pagination in action.
    """

    def pagination_in_action(self, queryset, ):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AddPreviousNextMixin:
    def get_object(self):
        obj = super().get_object()
        queryset = self.filter_queryset(self.get_queryset())
        try:
            # get ordering
            ordering_field = 'id'
            ordering_params = self.request.query_params.get('ordering', None)
            if ordering_params and hasattr(self, 'ordering_fields', ) and ordering_params in self.ordering_fields:
                ordering_field = ordering_params
            elif self.ordering:
                ordering_field = self.ordering
        except:
            ordering_field = 'id'
        descending = False
        if ordering_field.startswith('-'):
            ordering_field = ordering_field[1:]
            descending = True
        if descending:
            next_item = queryset.filter(**{f'{ordering_field}__lt': getattr(obj, ordering_field)}).order_by(
                f'-{ordering_field}').first()
            previous_item = queryset.filter(**{f'{ordering_field}__gt': getattr(obj, ordering_field)}).order_by(
                f'{ordering_field}').first()
        else:
            next_item = queryset.filter(**{f'{ordering_field}__gt': getattr(obj, ordering_field)}).order_by(
                f'{ordering_field}').first()
            previous_item = queryset.filter(**{f'{ordering_field}__lt': getattr(obj, ordering_field)}).order_by(
                f'-{ordering_field}').first()
        try:
            obj.next_item = getattr(next_item, self.lookup_field)
        except:
            obj.next_item = None
        try:
            obj.previous_item = getattr(previous_item, self.lookup_field)
        except:
            obj.previous_item = None
        return obj
