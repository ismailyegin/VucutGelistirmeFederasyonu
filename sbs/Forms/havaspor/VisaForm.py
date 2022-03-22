from django import forms
from django.forms import ModelForm

from sbs.models.havaspor.HavaLevel import HavaLevel


class VisaForm(ModelForm):

    class Meta:
        model =HavaLevel

        fields = (
            'dekont', 'branch', 'startDate')

        labels = {'branch': 'Branş', 'startDate': 'Geçerlilik yılı'}

        widgets = {

            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask2013', 'id': 'datepicker', 'autocomplete': 'on'}),
            'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

        }
