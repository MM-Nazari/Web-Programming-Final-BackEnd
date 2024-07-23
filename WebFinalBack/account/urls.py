from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework_nested import routers

router = DefaultRouter()
router.register(prefix='users', viewset=views.UserProfileModelViewset, basename="users")
users_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'contacts', views.ContactModelViewset, basename='user-contacts')

from . import views

urlpatterns = [

    path('login/', views.UserLoginApi.as_view(), name='login'),
    path('register/', views.UserRegisterApi.as_view(), name='signup'),
    path('', include(router.urls)),
    path('', include(users_router.urls)),
]
