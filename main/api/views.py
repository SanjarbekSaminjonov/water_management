import json
import datetime
import decimal
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import (
    ChannelDevice,
    ChannelMessage,
    ChannelDeviceVolumeTable,
    ChannelMovement,
)
from ..utils import send_message_to_admin, get_formatted_time


class ReceiveChannelDeviceMessageView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        h = data.get("h")
        bat = data.get("bat")
        is_charging = data.get("charging")
        net = data.get("net")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        device_id = data.get("device_id")
        taked = data.get("taked", 0)

        re_settings = data.get("re_settings", False)

        # Send logs to admin via telegram
        message = "Kanal qurilmasi xabarini qabul qilindi\n"
        message += str(json.dumps(data, indent=4))
        send_message_to_admin(message)

        device = ChannelDevice.objects.filter(device_id=device_id).first()
        if not device:
            return Response(
                {
                    "request": "error",
                    "message": "Device not found",
                    "datetime": get_formatted_time(datetime.datetime.now()),
                },
                status=404,
            )

        if int(taked):
            last_location = (
                ChannelMovement.objects.filter(device=device)
                .order_by("created_at")
                .last()
            )

            ChannelMovement.objects.create(
                device=device, latitude=latitude, longitude=longitude
            )

            device.latitude = latitude
            device.longitude = longitude
            device.save()
            send_message_to_admin(
                f"Kanal qurilmasi {device.name} {get_formatted_time(timezone.now())} vaqtda joylashuvi o'zgardi\n"
                f"Link: https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
            )
            return Response(
                {
                    "request": "success",
                    "datetime": get_formatted_time(datetime.datetime.now()),
                },
                status=201,
            )

        new_message = ChannelMessage.objects.create(
            device=device, h=h, bat=bat, is_charging=bool(int(is_charging)), net=net
        )

        if re_settings:
            device.full_height = device.height + decimal.Decimal(new_message.h)

        if device.full_height is not None:
            water_height = round(
                device.full_height - device.height_conf - decimal.Decimal(new_message.h)
            )
            device.height = water_height
            water_height_ones = water_height % 10
            water_height_tens = water_height - water_height_ones
            volume_row = (
                ChannelDeviceVolumeTable.objects.filter(device=device)
                .filter(tens=water_height_tens)
                .first()
            )
            if volume_row is not None:
                new_message.water_volume = volume_row.get_value(water_height_ones)
                new_message.save()

        device.latitude = latitude
        device.longitude = longitude
        device.save()
        return Response(
            {
                "request": "success",
                "datetime": get_formatted_time(timezone.now()),
            },
            status=201,
        )
