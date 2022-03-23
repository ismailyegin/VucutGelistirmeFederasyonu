from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from sbs.models.ekabis.CategoryItem import CategoryItem
from sbs.models.tvfbf.Coach import Coach
from sbs.models.tvfbf.Club import Club


class SearchClupForm(ModelForm):
    sportsClub = forms.ModelChoiceField(queryset=Club.objects.all(),
                                        to_field_name='name',
                                        empty_label="Seçiniz",
                                        label="Kulübü",
                                        required=False,
                                        widget=forms.Select(
                                            attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                   'style': 'width: 100%; '}))
    coach = forms.ModelChoiceField(queryset=Coach.objects.all(),
                                   # to_field_name='name',
                                   empty_label="Seçiniz",
                                   label="Antrenör",
                                   required=False,
                                   widget=forms.Select(
                                       attrs={'class': 'form-control select2 select2-hidden-accessible',
                                              'style': 'width: 100%; '}))

    class Meta:
        model =CategoryItem

        fields = (
            'sportsClub', 'branch')

        labels = { 'branch': 'Branş', 'sportsClub': 'Kulüp'}

        widgets = {



            'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%;'}),
            'sportsClub': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%;'}),

        }
