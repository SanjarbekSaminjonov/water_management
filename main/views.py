from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(generic.TemplateView):
    template_name = "home.html"


class ChannelDevicesView(LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        search = self.request.GET.get("search")
        qs = self.request.user.channel_devices.all()
        if search:
            qs = qs.filter(name__icontains=search)
        return qs
