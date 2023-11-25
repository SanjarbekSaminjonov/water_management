from django import forms
from django.forms import ModelForm
from .models import ChannelDevice, ChannelDeviceVolumeTable


class ChannelDeviceForm(ModelForm):
    device = forms.CharField(
        widget=forms.TextInput(attrs={"autocomplete": "off", "readonly": "readonly"}),
        error_messages={
            "required": "Device id bo'lishi shart",
            "invalid_choice": "Noto'g'ri device id kiritildi",
        },
    )

    class Meta:
        model = ChannelDevice
        fields = ("device", "name", "phone_number", "height")

    def __init__(self, *args, **kwargs):
        super(ChannelDeviceForm, self).__init__(*args, **kwargs)
        device_id = kwargs.pop("initial", {}).get("device")
        self.fields["device"].widget.attrs["value"] = device_id

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = (
                "w-full mt-2 mb-5 p-1 border-gray-900 rounded-md "
                "focus:border-indigo-600 focus:ring focus:ring-opacity-40"
                "focus:ring-indigo-500 border-2 border-black border-slate-500"
            )

    def save(self, master=None, commit=True):
        obj = super(ChannelDeviceForm, self).save(commit=False)
        if master:
            obj.master = master
        if commit:
            obj.save()
        return obj


class ChannelDeviceEditForm(ModelForm):
    class Meta:
        model = ChannelDevice
        fields = (
            "name",
            "phone_number",
            "ministry_id",
            "full_height",
            "height",
            "height_conf",
            "latitude",
            "longitude",
        )

    def __init__(self, *args, **kwargs):
        super(ChannelDeviceEditForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = (
                "w-full mt-2 mb-5 p-1 border-gray-900 rounded-md "
                "focus:border-indigo-600 focus:ring focus:ring-opacity-40"
                "focus:ring-indigo-500 border-2 border-black border-slate-500"
            )


class ChannelDeviceVolumeForm(ModelForm):
    class Meta:
        model = ChannelDeviceVolumeTable
        fields = (
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

    def __init__(self, *args, **kwargs):
        super(ChannelDeviceVolumeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = (
                "w-32 -mt-1 p-1 border-gray-900 rounded-md "
                "focus:border-indigo-600 focus:ring focus:ring-opacity-40"
                "focus:ring-indigo-500 border-2 border-black border-slate-500"
            )
