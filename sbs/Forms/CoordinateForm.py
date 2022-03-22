from django import forms

from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.Coordinate import Coordinate


class CoordinateForm(BaseForm):
    class Meta:
        model = Coordinate
        fields = ('x', 'y')

        labels = {'x': 'X Koordinatı ', 'y': 'Y Koordinatı'}
        widgets = {
            'x': forms.NumberInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'y': forms.NumberInput(attrs={'class': 'form-control ', 'required': 'required'}),

        }
