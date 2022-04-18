from django import forms
from django.forms import ModelForm

from sbs.models.tvfbf.Branch import Branch
from sbs.models.tvfbf.Club import Club
from sbs.models.tvfbf.SportClubUser import SportClubUser
from sbs.models.ekabis.City import City


class ClubSearchForm(ModelForm):
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
