from collections import OrderedDict
from collections.abc import Mapping

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SkipField, get_error_detail, set_value
from rest_framework.settings import api_settings

from core.message_txt import MessageTxt


class DjangoValidationError(BaseException):
    pass


class CustomBaseSerializer(serializers.Serializer):
    """Base Serializer for returning translated error"""

    # is_archived = serializers.HiddenField(required=False, default=False)
    # modified_date = serializers.HiddenField(required=False, default=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if hasattr(self, "fields"):
            for field in self.fields:
                self.fields[field].error_messages['required'] = MessageTxt.field_required(_(field))
                self.fields[field].error_messages['null'] = MessageTxt.field_required(_(field))
                self.fields[field].error_messages['blank'] = self.fields[field].error_messages['blank'] \
                    if 'blank' in self.fields[field].error_messages else MessageTxt.field_required(_(field))
                self.fields[field].error_messages['invalid'] = MessageTxt.field_invalid(_(field))

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def to_internal_value(self, data):
        """Dict of native values <- Dict of primitive data types."""
        if not isinstance(data, Mapping):
            message = self.error_messages['invalid'].format(
                datatype=type(data).__name__
            )
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='invalid')

        ret = OrderedDict()
        errors = OrderedDict()
        fields = self._writable_fields

        for field in fields:
            validate_method = getattr(self, 'validate_' + field.field_name, None)
            primitive_value = field.get_value(data)
            try:
                validated_value = field.run_validation(primitive_value)
                if validate_method is not None:
                    validated_value = validate_method(validated_value)
            except ValidationError as exc:
                errors[field.field_name] = exc.detail
            except DjangoValidationError as exc:
                errors[field.field_name] = get_error_detail(exc)
            except SkipField:
                pass
            else:
                if hasattr(field, 'remove_parent') and field.remove_parent:
                    for key, value in validated_value.items():
                        ret[key] = value
                else:
                    set_value(ret, field.source_attrs, validated_value)
        if errors:
            raise ValidationError(errors)
        return ret


class BaseModelSerializer(CustomBaseSerializer,
                          serializers.ModelSerializer):
    """
    Base Model Serializer that can be used to serialize
    """
    pass


class EmptyPayloadResponseSerializer(CustomBaseSerializer):
    """
    that use to resolve swagger error
    """
    detail = serializers.CharField()
