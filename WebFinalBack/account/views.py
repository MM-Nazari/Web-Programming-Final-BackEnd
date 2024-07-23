from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from account.filters import UserFilter
from account.models import User, Contact
from account.permissions import IsOwnerPermission
from account.serializers import TokenObtainPairSerializer, UserSerializer, ContactSerializer
from core.base_view import CustomGenericMixin


class UserLoginApi(TokenObtainPairView):
    """
    login api to get token.use mobile or national code and password to login.and return a token.
    """
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializer


class UserRegisterApi(CreateAPIView):
    """
    register api to get token.use mobile or user_name and password to register.and return a token.
    """
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class UserProfileModelViewset(CustomGenericMixin,
                              mixins.ListModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin,
                              GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    filter_backends = [filters.DjangoFilterBackend, ]
    filterset_class = UserFilter

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerPermission]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_destroy(self, instance):
        """
        set is_active to False
        """

        instance.is_active = False
        instance.save()


class ContactModelViewset(CustomGenericMixin,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


