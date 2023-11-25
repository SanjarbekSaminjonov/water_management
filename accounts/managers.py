from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    @staticmethod
    def normalize_phone_number(phone_number):
        return phone_number.replace(" ", "")

    @staticmethod
    def validate_phone_number(phone_number):
        if not phone_number.startswith("+998"):
            raise ValueError(_("phone number must start with +998"))
        if not phone_number[1:].isdigit():
            raise ValueError(_("phone number must be digit"))
        if len(phone_number) != 13:
            raise ValueError(_("phone number must be 11 digit"))

    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError(_("the phone number must be set"))

        phone_number = self.normalize_phone_number(phone_number)
        self.validate_phone_number(phone_number)

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("superuser must have is_superuser=True."))

        return self.create_user(
            phone_number=phone_number, password=password, **extra_fields
        )
