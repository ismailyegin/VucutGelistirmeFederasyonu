

from django import forms

from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.CompanyFileNames import CompanyFileNames
class CompanyFileNameForm(BaseForm):
    class Meta:
        model = CompanyFileNames
        fields = (
            'name',
            'is_active',

        )
        labels = {'name': 'İsim',
                  'is_active': 'Alan Türü',

                  }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'is_active': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; ', 'required': 'required'}),
        }