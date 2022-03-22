from django import forms

from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.YekaBussiness import YekaBusiness

class YekaBusinessForm(BaseForm):
    class Meta:
        model = YekaBusiness
        fields = ('name', )

        labels = {'Name': 'Tanım ', }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

        }