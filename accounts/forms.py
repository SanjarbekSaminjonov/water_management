from django.contrib.auth.forms import UserChangeForm as DefaultUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DefaultUserCreationForm

from .models import User


class UserCreationForm(DefaultUserCreationForm):
    class Meta:
        model = User
        fields = ("phone_number", "first_name", "last_name")


class UserChangeForm(DefaultUserChangeForm):
    class Meta:
        model = User
        fields = (
            "phone_number",
            "first_name",
            "last_name",
            "role",
            "is_staff",
            "is_superuser",
        )
