from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from account.models import User
#from account.serializers import UserBaseSerializer
from core.base_exception import NotFoundException, PermissionDeniedException
from core.base_serializer import BaseModelSerializer
#from core.choice_field_types import FileCategory
from core.message_txt import MessageTxt
from core.models import Document, FileType


class FileTypeSerializer(BaseModelSerializer):
    class Meta:
        model = FileType
        fields = ('id', 'name', 'name_en', 'category', 'priority')

    def validate(self, attrs):
        attrs['owner'] = self.context['request'].user
        return super().validate(attrs)


class DocumentSerializer(BaseModelSerializer):
    file_type_id = serializers.PrimaryKeyRelatedField(queryset=FileType.objects.all(),
                                                      source='file_type', write_only=True)
    file_type = FileTypeSerializer(read_only=True)

    class Meta:
        model = Document
        fields = ('id', 'file_type_id', 'file_type', 'file', 'state', 'alt')
        read_only_fields = ('state',)  # TODO:Maybe change in future

    def _check_file_type(self, validated_data):
        file_type = validated_data.get('file_type')
        # if category in individual, non_citizen and legal base on file_type.name_en user just can have one file
        if file_type.category in [FileCategory.INDIVIDUAL, FileCategory.NON_CITIZEN, FileCategory.LEGAL]:
            document = Document.objects.filter(owner=validated_data['owner'],
                                               file_type__name_en=file_type.name_en)
            if document.exists():
                return super().update(document.first(), validated_data)
        return super().create(validated_data)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if self.context['request'].user.is_authenticated:
            validated_data['owner'] = self.context['request'].user
        if validated_data['file_type'].category in [FileCategory.PUBLIC, FileCategory.STORAGE]:
            raise PermissionDeniedException
        return validated_data

    def create(self, validated_data):
        return self._check_file_type(validated_data)


class AdminDocumentSerializer(DocumentSerializer):
    owner_id = serializers.IntegerField(write_only=True, required=False)
    owner = UserBaseSerializer(read_only=True)

    class Meta(DocumentSerializer.Meta):
        fields = DocumentSerializer.Meta.fields + ('owner', 'owner_id')

    def _check_owner(self, validated_data):
        owner_id = validated_data.pop('owner_id', None)
        pre_owner = getattr(self.instance, 'owner', None)
        if not owner_id and not pre_owner:
            validated_data['owner'] = self.context['request'].user
        if owner_id:
            validated_data['owner'] = User.objects.get(id=owner_id)
        return validated_data

    def validate(self, validated_data):
        try:
            validated_data = self._check_owner(validated_data)
            return ModelSerializer().validate(validated_data)
        except User.DoesNotExist:
            raise NotFoundException(MessageTxt.LoginFailNoUser401)
