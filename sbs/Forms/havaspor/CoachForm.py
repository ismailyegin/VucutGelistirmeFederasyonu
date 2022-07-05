from django import forms
from django.forms import ModelForm
from sbs.models import Coach


class CoachForm(ModelForm):
    class Meta:
        model = Coach

        fields = ('sgk', 'antrenorBelgesi', 'form')
        labels = {
            'sgk': 'SGK Belgesi', 'antrenorBelgesi': 'Antrenör Belgesi', 'form': 'Antrenör Sözleşme Belgesi'

        }
        widgets = {

        }
