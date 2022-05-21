from django import forms

from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.Communication import Communication


class ProfileCommunicationForm(BaseForm):

    class Meta:
        model = Communication

        fields = (
            'phoneNumber', 'address', 'postalCode', 'country', 'city','phoneNumber2'
            )
        labels = {'phoneNumber': 'Cep Telefonu',
                  'phoneNumber2': 'Sabit Telefon',
                   'address':'Adres',
                  'postalCode': 'Posta Kodu',
                  'city': 'İl',
                  'country':'Ülke'}
        widgets = {

            'phoneNumber': forms.TextInput(
                attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),
            'address': forms.TextInput(
                attrs={'class': 'form-control ',}),
            'postalCode': forms.TextInput(
                attrs={'class': 'form-control ',}),
            'phoneNumber2': forms.TextInput(
                attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),

            'city': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%; ', 'name': "city", 'id': "id_city"}),
            'country': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%; ', 'name': "city", 'id': "id_city"}),


        }
