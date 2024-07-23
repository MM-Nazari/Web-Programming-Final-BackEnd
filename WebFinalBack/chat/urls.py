from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework_nested import routers

router = DefaultRouter()
router.register(prefix='chats', viewset=views.ChatModelViewset, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
]



