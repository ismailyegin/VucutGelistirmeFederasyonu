from django import forms

from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.YekaApplicationFileName import YekaApplicationFileName


class YekaApplicationFileNameForm(BaseForm):
    class Meta:
        model = YekaApplicationFileName
        fields = ('filename',)
        labels = {'filename': 'İsim',}
        widgets = {
            'filename': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'required'}),

        }
