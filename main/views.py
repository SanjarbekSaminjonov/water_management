from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import redirect


class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = "home.html"


class ChannelDevicesView(LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        search = self.request.GET.get("search")
        qs = self.request.user.channel_devices.all()
        if search:
            qs = qs.filter(name__icontains=search)
        return qs


class ChannelDeviceDetailView(LoginRequiredMixin, generic.DetailView):
    slug_field = "device_id"
    slug_url_kwarg = "device_id"

    def get_queryset(self):
        return self.request.user.channel_devices.all()

    def get_context_data(self, **kwargs):
        cut = 10
        context = super().get_context_data(**kwargs)
        messages = self.object.messages
        device_messages = messages.order_by("-created_at")[:cut]
        has_more = messages.count() > cut
        location = dict(
            latitude=str(self.object.latitude),
            longitude=str(self.object.longitude),
        )
        context.update(
            device_messages=device_messages, has_more=has_more, location=location
        )
        return context


class ChannelDeviceDeleteView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        device_id = kwargs.get("device_id")
        qs = self.request.user.channel_devices.filter(device_id=device_id)
        if qs.exists():
            qs.first().delete()
        return redirect("main:channeldevices")


class ChannelDeviceVolumeTableView(LoginRequiredMixin, generic.DetailView):
    slug_field = "device_id"
    slug_url_kwarg = "device_id"
    template_name = "main/channeldevice_volume_table.html"

    def get_queryset(self):
        return self.request.user.channel_devices.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        volume_table = self.object.volume_tables.order_by("tens")
        context.update(volume_table=volume_table)
        return context
