from django import forms

from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.Person import Person


class PersonForm(BaseForm):
    class Meta:
        model = Person

        fields = (
            'tc', 'profileImage', 'iban', )
        labels = {'tc': 'T.C. *', 'profileImage': 'Profil Resmi'}

        widgets = {


            'tc': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required', 'maxlength': '11', 'minlength': '11',
                       'onkeypress': 'validate(event)', 'name': 'tc', 'id': 'tc'}),

        }
