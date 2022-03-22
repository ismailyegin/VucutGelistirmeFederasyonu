
from django import forms

from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.ExtraTimeFile import ExtraTimeFile

class ExtraTimeFileForm(BaseForm):
    class Meta:
        model = ExtraTimeFile
        fields = ('definition','file')
        labels = {'definition': 'Açıklama '}
        widgets = {
            'definition': forms.TextInput(
                attrs={'class': 'form-control ',}),
        }