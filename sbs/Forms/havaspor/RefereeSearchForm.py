from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from sbs.models.ekabis.CategoryItem import CategoryItem
from sbs.models.ekabis.City import City
from sbs.models.tvfbf.Branch import Branch


class RefereeSearchForm(ModelForm):
    # kademe
    status = forms.ModelChoiceField(queryset=CategoryItem.objects.filter(forWhichClazz='REFEREE_GRADE'),
                                        to_field_name='name',
                                        empty_label="Seçiniz",
                                        label="Kademe",
                                        required=False,
                                        widget=forms.Select(
                                            attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                   'style': 'width: 100%; '}))
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(),
                                    to_field_name='title',
                                    empty_label="Seçiniz",
                                    label="Branş",
                                    required=False,
                                    widget=forms.Select(
                                        attrs={'class': 'form-control select2 select2-hidden-accessible',
                                               'style': 'width: 100%; '}))
    city = forms.ModelChoiceField(queryset=City.objects.all().distinct(),
                                  to_field_name='name',
                                  empty_label="Seçiniz",
                                  label="Şehir",
                                  required=False,
                                  widget=forms.Select(
                                      attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%; '}))

    #  'onchange': 'this.form.submit()' ile ajax yazilabilir not
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)
        labels = {'first_name': 'Ad', 'last_name': 'Soyad'}
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': ' Ad', 'value': '', "style": "text-transform:uppercase"
                       }),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': ' Soyad', "style": "text-transform:uppercase"}),

        }


