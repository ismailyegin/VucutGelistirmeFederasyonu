from django import forms
from django.forms import ModelForm

from sbs.models.ekabis.CategoryItem import CategoryItem
from sbs.models.tvfbf.HavaLevel import HavaLevel


class GradeFormCoach(ModelForm):
    definition = forms.ModelChoiceField(queryset=CategoryItem.objects.filter(forWhichClazz='COACH_GRADE').order_by('order'),
                                               to_field_name='name',
                                               empty_label="Seçiniz",
                                               label="Kademe",
                                               required='required',
                                               widget=forms.Select(
                                                   attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                          'style': 'width: 100%; '}))

    class Meta:
        model = HavaLevel

        fields = (
            'startDate', 'definition','branch', 'dekont', 'form')

        labels = {'startDate': 'Hak Kazanma Tarihi', 'branch': 'Branş', 'form': 'Kademe Belgesi', 'dekont': 'Dekont'}

        widgets = {

             'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'on',
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),
             'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.initial['form']:
    #         self.fields['form'].widget.attrs['readonly'] = 'readonly'
    #     if self.initial['branch']:
    #         self.fields['branch'].widget.attrs['readonly'] = 'readonly'
    #     if self.initial['dekont']:
    #         self.fields['dekont'].widget.attrs['readonly'] = 'readonly'
    #     if self.initial['startDate']:
    #         self.fields['startDate'].widget.attrs['readonly'] = 'readonly'
    #         self.fields['startDate'].widget.attrs['required'] = False
    #
    #     if self.initial['definition']:
    #         self.fields['definition'].widget.attrs['readonly'] = 'readonly'
