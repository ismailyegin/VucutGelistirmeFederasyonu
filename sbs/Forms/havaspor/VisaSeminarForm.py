from django import forms
from django.forms import ModelForm
from sbs.models.havaspor.VisaSeminar import VisaSeminar


class VisaSeminarForm(ModelForm):
    class Meta:
        model = VisaSeminar
        fields = (
            'name', 'startDate', 'finishDate', 'location', 'branch', 'year')
        labels = {'name': 'İsim', 'startDate': 'Başlangıç Tarihi', 'finishDate': 'Bitiş Tarihi',
                  'location': 'Yer', 'branch': 'Branş', 'year': 'Geçerlilik yılı '}
        widgets = {
            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker2', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'finishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker4', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'year': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker5', 'autocomplete': 'on',
                       'onkeydown': 'return true', 'required': 'required'}),
            'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),

            'location': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),

        }
