from django import forms
from django.forms import ModelForm

from sbs.Forms.BaseForm import BaseForm
from sbs.models.tvfbf.DocumentName import DocumentName


class DocumentNameForm(BaseForm):
    class Meta:
        model = DocumentName
        fields = ('name',)
        labels = {'name': 'Belge Adı', }
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
        }
