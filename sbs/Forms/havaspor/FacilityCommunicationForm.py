from django import forms
from django.forms import ModelForm

from sbs.models import Communication
from sbs.models.ekabis.Country import Country


class FacilityCommunicationForm(ModelForm):
    class Meta:
        model = Communication

        fields = (
            'phoneNumber', 'city'
            , 'address', 'town')
        labels = {'phoneNumber': 'Cep Telefonu',
                  'address': 'Adres',
                  'city': 'İl', 'town': 'İlçe'}
        widgets = {

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '1', "style": "text-transform:uppercase"}),

            'phoneNumber': forms.TextInput(
                attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;'}),



            'town': forms.TextInput(attrs={'class': 'form-control',}),

        }
