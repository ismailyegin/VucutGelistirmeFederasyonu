from django import forms
from django.forms import ModelForm

from sbs.models import Communication
from sbs.models.ekabis.Country import Country


class CommunicationForm(ModelForm):
    class Meta:
        model = Communication

        fields = (
            'phoneNumber', 'country', 'city', 'phoneNumber2'
            , 'address',)
        labels = {'phoneNumber': 'Cep Telefonu', 'phoneNumber2': 'Sabit Telefon',
                  'address': 'Adres',
                  'city': 'İl', 'country': 'Ülke'}
        widgets = {

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '2'}),

            'phoneNumber': forms.TextInput(
                attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;'}),

            'country': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%;'}),

            'phoneNumber2': forms.TextInput(attrs={'class': 'form-control', 'onkeypress': 'validate(event)'}),

        }
