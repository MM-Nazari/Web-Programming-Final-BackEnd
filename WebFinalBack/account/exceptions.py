from rest_framework import status

from core.base_exception import BaseApiException
from core.message_txt import MessageTxt


class LoginFailException(BaseApiException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = MessageTxt.LoginFailNoUser401
    default_code = 4001


class InputValidDataException(BaseApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = MessageTxt.InputValidData
    default_code = 4002


class InvalidInputException(BaseApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = MessageTxt.InvalidInput400
    default_code = 4003


class NotFoundException(BaseApiException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = MessageTxt.NotFound404
    default_code = 4004


class UniqueMobileException(BaseApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = MessageTxt.UniqueMobile
    default_code = 4005


class WrongPasswordException(BaseApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = MessageTxt.WrongPassword400
    default_code = 4007


class UserNotActiveException(BaseApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = MessageTxt.UserNotActive
    default_code = 4008
