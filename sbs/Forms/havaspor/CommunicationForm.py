from django import forms
from django.forms import ModelForm

from sbs.models import Communication
from sbs.models.ekabis.Country import Country


class CommunicationForm(ModelForm):
    class Meta:
        model = Communication

        fields = (
            'phoneNumber', 'country', 'city', 'phoneJop'
            , 'address',)
        labels = {'phoneNumber': 'Cep Telefonu', 'phoneJop': 'Sabit Telefon',
                  'address': 'Adres',
                  'city': 'İl', 'country': 'Ülke'}
        widgets = {

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '1', "style": "text-transform:uppercase"}),

            'phoneNumber': forms.TextInput(
                attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;'}),

            'country': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%;'}),

            'phoneJop': forms.TextInput(attrs={'class': 'form-control', 'onkeypress': 'validate(event)'}),

        }
