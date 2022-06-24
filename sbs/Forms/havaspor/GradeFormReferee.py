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
             'definition', 'form', 'branch')

        labels = {'branch': 'Branş','form':'Kademe Belgesi'}

        widgets = {


            'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

        }
