from django.urls import path

from . import views
from .api.views import ReceiveChannelDeviceMessageView

app_name = "main"

urlpatterns = [
    path(
        "api/channeldevices/messages/",
        ReceiveChannelDeviceMessageView.as_view(),
        name="api_channeldevice_messages",
    ),
    path("", views.HomeView.as_view(), name="home"),
    path("channeldevices/", views.ChannelDevicesView.as_view(), name="channeldevices"),
    path(
        "channeldevices/<str:device_id>/",
        views.ChannelDeviceDetailView.as_view(),
        name="channeldevice_detail",
    ),
    path(
        "channeldevices/<str:device_id>/delete/",
        views.ChannelDeviceDeleteView.as_view(),
        name="channeldevice_delete",
    ),
]
