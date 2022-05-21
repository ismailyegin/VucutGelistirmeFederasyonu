from django import forms
from django.forms import ModelForm
from sbs.models import Coach


class CoachForm(ModelForm):
    class Meta:
        model = Coach

        fields = ('sgk',)
        labels = {
            'sgk': 'SGK Belgesi',


        }
        widgets = {

        }
