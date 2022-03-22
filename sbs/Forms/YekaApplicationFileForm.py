from django import forms
from django.forms import ModelForm

from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.YekaApplicationFile import YekaApplicationFile


class YekaApplicationFileForm(BaseForm):
    class Meta:
        model = YekaApplicationFile
        fields = ('file',)
        labels = {'file': 'Dosya',}

