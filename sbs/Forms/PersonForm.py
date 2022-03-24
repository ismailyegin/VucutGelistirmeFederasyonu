from django import forms

from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.Person import Person


class PersonForm(BaseForm):
    class Meta:
        model = Person

        fields = (
            'tc', 'profileImage', 'iban','birthDate',)
        labels = {'tc': 'T.C. *', 'profileImage': 'Profil Resmi',}

        widgets = {


            'tc': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required', 'maxlength': '11', 'minlength': '11',
                       'onkeypress': 'validate(event)', 'name': 'tc', 'id': 'tc'}),
            'birthDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker6', 'autocomplete': 'off',
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),

        }
