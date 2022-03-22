from django import forms

from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.ConnectionUnit import ConnectionUnit


class ConnectionUnitForm(BaseForm):
    class Meta:
        model = ConnectionUnit
        fields = ('name',)

        labels = {'name': 'Birim '}
        widgets = {
             'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
         }
