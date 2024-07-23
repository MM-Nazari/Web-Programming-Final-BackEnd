from rest_framework import response
from rest_framework.pagination import PageNumberPagination
from rest_framework.settings import api_settings


class CustomPaginator(PageNumberPagination):
    """Custom pagination """

    def paginate_queryset(self, queryset, request, view=None):
        """ determine the number of records should be shown dynamically. base on page_size parameter"""
        self.page_size = request.query_params.get('page_size') if request.query_params.get(
            'page_size') else api_settings.PAGE_SIZE
        return super().paginate_queryset(queryset, request)

    def get_paginated_response(self, data):
        return response.Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'last_page': self.page.paginator.page_range.stop - 1,
            'page_size': self.page_size,
            'current_page_no': self.page.number,
            'results': data,
        })
