from collections import namedtuple

from rest_framework.permissions import IsAuthenticated, BasePermission

from nzari import settings

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsStaffPermission(IsAuthenticated):
    """
    check user is staff or superuser
    """

    def has_permission(self, request, view):
        try:
            return request.user.is_admin
        except Exception as e:
            return False

    def has_object_permission(self, request, view, obj):
        try:
            return request.user.is_admin
        except Exception as e:
            return False


class IsOwnerPermission(IsAuthenticated):
    """
    for create,list  user must be authenticated
    for other method ,check user is owner of object , superuser or staff can access all objects
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        try:
            return request.user.is_admin or request.user == obj
        except Exception as e:
            return False


