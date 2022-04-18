from django import forms
from django.forms import ModelForm

from sbs.models.ekabis.Communication import Communication
from sbs.models.ekabis.Country import Country


class TransCommunicationForm(ModelForm):
    class Meta:
        model = Communication

        fields = (
             'city','town', 'address','phoneNumber', 'fax',)
        labels = {'phoneNumber': 'Cep Telefonu', 'phoneJop': 'Sabit Telefon',
                  'address': 'Adres',
                  'city': 'İl', 'fax': 'Faks','town':'İlçe'}
        widgets = {

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '2', 'readonly': 'readonly'}),

            'phoneNumber': forms.TextInput(
                attrs={'class': 'form-control ', 'readonly': 'readonly'}),
            'fax': forms.TextInput(
                attrs={'class': 'form-control ', 'readonly': 'readonly'}),

            'city': forms.TextInput(attrs={'class': 'form-control',
                                           'readonly': 'readonly'}),
            'town': forms.TextInput(attrs={'class': 'form-control',
                                           'readonly': 'readonly'}),



        }
