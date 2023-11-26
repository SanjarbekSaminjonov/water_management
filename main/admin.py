from django.contrib import admin

from .models import (
    ChannelDevice,
    ChannelDeviceVolumeTable,
    ChannelMessage,
    ChannelMovement,
)


@admin.register(ChannelDevice)
class ChannelDeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "device_id", "owner")
    list_display_links = ("id", "name")
    list_filter = ("owner",)
    search_fields = ("name", "device_id")
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("owner",)


@admin.register(ChannelDeviceVolumeTable)
class ChannelDeviceVolumeTableAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "device",
        "tens",
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    )
    list_display_links = ("id", "device")
    list_filter = ("device", "created_at")
    search_fields = ("device",)
    raw_id_fields = ("device",)


@admin.register(ChannelMessage)
class ChannelMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "device", "is_sent", "h", "water_volume")
    list_display_links = ("id", "device")
    list_filter = ("device", "created_at")
    search_fields = ("device",)
    raw_id_fields = ("device",)


@admin.register(ChannelMovement)
class ChannelMovementAdmin(admin.ModelAdmin):
    list_display = ("id", "device", "created_at", "latitude", "longitude")
    list_display_links = ("id", "device")
    list_filter = ("device", "created_at")
    search_fields = ("device",)
    raw_id_fields = ("device",)
