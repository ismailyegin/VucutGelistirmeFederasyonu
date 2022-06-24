from django import forms
from django.forms import ModelForm

from sbs.models.tvfbf.HavaLevel import HavaLevel


class VisaForm(ModelForm):
    class Meta:
        model = HavaLevel

        fields = ('branch', 'dekont', )

        labels = {'branch': 'Branş', 'dekont': 'Dekont', }

        widgets = {

            'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),



        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.initial['form']:
    #         self.fields['form'].widget.attrs['readonly'] = 'readonly'
    #     if self.initial['branch']:
    #         self.fields['branch'].widget.attrs['readonly'] = 'readonly'
    #         self.fields['branch'].widget.attrs['required'] = False
    #
    #     if self.initial['dekont']:
    #         self.fields['dekont'].widget.attrs['readonly'] = 'readonly'
    #     if self.initial['startDate']:
    #         self.fields['startDate'].widget.attrs['readonly'] = 'readonly'
    #         self.fields['startDate'].widget.attrs['required'] = False
