from django import forms
from django.forms import ModelForm

from sbs.models.ekabis.CategoryItem import CategoryItem
from sbs.models.tvfbf.HavaLevel import HavaLevel


class GradeFormReferee(ModelForm):
    definition = forms.ModelChoiceField(queryset=CategoryItem.objects.filter(forWhichClazz='REFEREE_GRADE'),
                                        to_field_name='name',
                                        empty_label="Seçiniz",
                                        label="Kademe",
                                        widget=forms.Select(
                                            attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                   'style': 'width: 100%; '}))

    class Meta:
        model = HavaLevel

        fields = (
            'definition', 'branch', 'gradeDate', 'gradeNo', 'referee_file')

        labels = {'gradeDate': 'Hak Kazanma Tarihi', 'branch': 'Branş', 'gradeNo': 'Kokart No',
                  'referee_file': 'Hakem Belgesi'}

        widgets = {

            'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

            'gradeDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'on',
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),

            'gradeNo': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),

        }
