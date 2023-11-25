from datetime import timedelta
from django.utils import timezone
from django.db import models
from accounts.models import User


class ChannelDevice(models.Model):
    device_id = models.CharField(
        verbose_name="Qurilma ID raqami",
        max_length=20,
        unique=True,
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Nomi",
    )
    ministry_id = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Vazirlikdagi ID raqami",
    )
    permission_to_send = models.BooleanField(
        default=False,
        verbose_name="Ma'lumotlar vazirlikka yuborilsinmi?",
    )
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="channel_devices",
        verbose_name="Qurilma egasi",
    )
    phone_number = models.CharField(
        verbose_name="Qurilmadagi sim karta raqami",
        max_length=20,
        blank=True,
    )
    full_height = models.DecimalField(
        default=0.0,
        max_digits=8,
        decimal_places=2,
        verbose_name="Suv tubidan sensorgacha balandlik (sm)",
    )
    height = models.DecimalField(
        default=0.0,
        max_digits=8,
        decimal_places=2,
        verbose_name="Suv sathi balandligi (sm)",
    )
    height_conf = models.IntegerField(
        default=0,
        blank=True,
        verbose_name="Tuzatish koffitsenti (sm)",
    )
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        verbose_name="Joylashuv (latitude)",
        blank=True,
        null=True,
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        verbose_name="Joylashuv (longitude)",
        blank=True,
        null=True,
    )

    updated_at = models.DateTimeField(
        verbose_name="O'zgartirilgan vaqti",
        auto_now=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Qo'shilgan vaqti",
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.name} - {self.device_id}"

    class Meta:
        verbose_name = "Kanal qurilmasi"
        verbose_name_plural = "Kanal qurilmalari"


class ChannelDeviceVolumeTable(models.Model):
    device = models.ForeignKey(
        to=ChannelDevice,
        on_delete=models.CASCADE,
        related_name="volume_tables",
        verbose_name="Kanal qurilmasi",
    )
    tens = models.IntegerField(
        default=0,
        verbose_name="O'nlik",
    )
    zero = models.FloatField(default=0, verbose_name="0")
    one = models.FloatField(default=0, verbose_name="1")
    two = models.FloatField(default=0, verbose_name="2")
    three = models.FloatField(default=0, verbose_name="3")
    four = models.FloatField(default=0, verbose_name="4")
    five = models.FloatField(default=0, verbose_name="5")
    six = models.FloatField(default=0, verbose_name="6")
    seven = models.FloatField(default=0, verbose_name="7")
    eight = models.FloatField(default=0, verbose_name="8")
    nine = models.FloatField(default=0, verbose_name="9")

    updated_at = models.DateTimeField(
        verbose_name="O'zgartirilgan vaqti",
        auto_now=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Qo'shilgan vaqti",
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.id} / {self.device} / {self.tens}"

    def get_value(self, ones):
        match_values = {
            0: self.zero,
            1: self.one,
            2: self.two,
            3: self.three,
            4: self.four,
            5: self.five,
            6: self.six,
            7: self.seven,
            8: self.eight,
            9: self.nine,
        }
        return match_values.get(ones)

    class Meta:
        verbose_name = "Kanal qurilmasi hajm jadvali"
        verbose_name_plural = "Kanal qurilmasi hajm jadvali"


class ChannelMessage(models.Model):
    device = models.ForeignKey(
        to=ChannelDevice,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Kanal qurilmasi",
    )
    is_sent = models.BooleanField(
        verbose_name="Yuborildimi?",
        default=False,
    )
    h = models.DecimalField(
        verbose_name="Qurilmadan suv yuzigacha balandlik (sm)",
        max_digits=7,
        decimal_places=2,
    )
    water_volume = models.DecimalField(
        verbose_name="Suv hajmi (m3/s)",
        max_digits=12,
        decimal_places=2,
    )
    bat = models.DecimalField(
        verbose_name="Batareya quvvat darajasi",
        max_digits=3,
        decimal_places=2,
        default=0,
    )
    is_charging = models.BooleanField(
        verbose_name="Batareya quvvatlanmoqda?",
        default=False,
    )
    net = models.IntegerField(
        verbose_name="Tarmoq signal darajasi",
        default=0,
    )
    created_at = models.DateTimeField(
        verbose_name="Qo'shilgan vaqti",
        auto_now_add=True,
    )

    def __str__(self):
        return self.device.name

    def get_water_height(self):
        return (
            self.device.full_height - self.h
            if self.device.full_height
            else self.device.height
        )

    def get_device_active(self):
        return timezone.now() - self.created_at < timedelta(days=1)

    class Meta:
        verbose_name = "Kanal qurilmasi xabari"
        verbose_name_plural = "Kanal qurilmasi xabarlari"


class ChannelMovement(models.Model):
    device = models.ForeignKey(
        to=ChannelDevice,
        on_delete=models.CASCADE,
        related_name="movements",
        verbose_name="Kanal qurilmasi",
    )
    latitude = models.DecimalField(
        verbose_name="Joylashuv (latitude)",
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
    )
    longitude = models.DecimalField(
        verbose_name="Joylashuv (longitude)",
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Qo'shilgan vaqti",
        auto_now_add=True,
    )

    def __str__(self):
        return self.device.name

    class Meta:
        verbose_name = "Kanal qurilmasi siljish xabari"
        verbose_name_plural = "Kanal qurilmasi siljish xabarlari"
