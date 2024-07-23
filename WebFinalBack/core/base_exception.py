from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details

from core.message_txt import MessageTxt


class BaseApiException(APIException):
    """
    for raising Exception define your exception with this structure:
        class SampleException(BaseApiException):
            status_code = status.HTTPStatusCode
            default_detail = error message
            default_code = code
    """

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)


class BadRequestException(BaseApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = MessageTxt.BadRequest400
    default_code = 400


class UnauthorizedException(BaseApiException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = MessageTxt.LoginFailNoUser401
    default_code = 401


class PermissionDeniedException(BaseApiException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = MessageTxt.DontHavePermission403
    default_code = 403


class NotFoundException(BaseApiException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = MessageTxt.NotFound404
    default_code = 404
