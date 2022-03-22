from django import forms
from django.forms import ModelForm

from sbs.models.havaspor.Branch import Branch
from sbs.models.havaspor.Club import Club
from sbs.models.havaspor.SportClubUser import SportClubUser
from sbs.models.ekabis.City import City


class ClubSearchForm(ModelForm):
    kisi = forms.ModelChoiceField(queryset=SportClubUser.objects.all().distinct(),
                                  to_field_name='user',
                                  empty_label="Seçiniz",
                                  label="Kulüp Yetkilisi",
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

    branch = forms.ModelChoiceField(queryset=Branch.objects.all(),
                                  to_field_name='title',
                                  empty_label="Seçiniz",
                                  label="Branş",
                                  required=False,
                                  widget=forms.Select(
                                      attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%; '}))
    class Meta:
        model = Club

        fields = (
            'name', 'shortName', 'clubMail')

        labels = {
            'name': 'Kulüp Adı',
            'shortName': 'Kulüp Kısa Adı',
            'clubMail': 'Kulüp Email',

        }
        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control', "style": "text-transform:uppercase"}),

            # 'shortName': forms.TextInput(attrs={'class': 'form-control'}),

            'clubMail': forms.TextInput(attrs={'class': 'form-control'}),


        }
