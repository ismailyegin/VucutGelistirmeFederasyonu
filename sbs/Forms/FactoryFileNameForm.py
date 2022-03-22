from django import forms
from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.FactoryFileName import FactoryFileName


class FactoryFileNameForm(BaseForm):
    class Meta:
        model = FactoryFileName
        fields = ('name',)
        labels = {'name': 'Doküman İsmi', }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

        }
