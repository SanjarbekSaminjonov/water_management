from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager


class UserRole(models.Model):
    name = models.CharField("Nomi", max_length=50)
    code = models.CharField("Kodi", max_length=50)
    updated_at = models.DateTimeField("O'zgartirilgan vaqti", auto_now=True)
    created_at = models.DateTimeField("Yaratilgan vaqti", auto_now_add=True)

    class Meta:
        verbose_name = "Lavozim"
        verbose_name_plural = "Lavozimlar"


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField("Telefon raqam", max_length=20, unique=True)
    first_name = models.CharField("Ism", max_length=50)
    last_name = models.CharField("Familiya", max_length=50)
    role = models.ForeignKey(
        UserRole,
        verbose_name="Lavozim",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_staff = models.BooleanField("Hodim", default=False)
    password = models.CharField("Parol", max_length=128, blank=True)
    last_login = models.DateTimeField("Oxirgi kirish", blank=True, null=True)
    date_joined = models.DateTimeField("Ro'yxatdan o'tish vaqti", default=timezone.now)
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"
