from django import forms
from sbs.models.ekabis.CompetitionApplication import CompetitionApplication


class YekaApplicationForm(forms.ModelForm):
    class Meta:
        model = CompetitionApplication
        fields = ('startDate', 'finishDate','preRegistration',)
        labels = {'startDate': 'Basvuru Başlangıç Tarihi',
                  'finishDate': 'Basvuru Bitiş Tarihi',
                  'preRegistration': 'Basvuru Aç'}
        widgets = {
            'preRegistration': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),
            'startDate':forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return true',  "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),
            'finishDate':forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker4', 'autocomplete': 'off',
                       'onkeydown': 'return true',  "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),

        }
