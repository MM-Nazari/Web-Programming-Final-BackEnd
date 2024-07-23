import django_filters

from account.models import User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'id': ['exact'],
            'first_name': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains'],
            'phone': ['exact', 'icontains'],
            'user_name': ['exact', 'icontains'],

        }
