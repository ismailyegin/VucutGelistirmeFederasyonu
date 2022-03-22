from django import forms
from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.CompetitionCompany import CompetitionCompany


class CompetitionCompanyForm(BaseForm):

    class Meta:
        model = CompetitionCompany
        fields = (
            'price',
            'company',
        )
        labels = {'price': 'Fiyat',
                  'company':'Firma'
                  }
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),
            'price': forms.NumberInput(
                attrs={'class': 'form-control ','required': 'required'}),
        }
