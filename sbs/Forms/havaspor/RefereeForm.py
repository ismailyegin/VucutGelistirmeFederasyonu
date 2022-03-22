from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from sbs.models.havaspor.Referee import Referee
from sbs.models.havaspor.Branch import Branch


class RefereeForm(ModelForm):
    class Meta:
        model = Referee

        fields = ('nufusCuzdani', 'diploma', 'sabikaKaydi', 'cezaYazisi', 'saglikBeyanFormu', 'hakemBilgiFormu',)
        labels = {
            'nufusCuzdani': 'Nüfus Cüzdanı',
            'diploma': 'Diploma',
            'sabikaKaydi': 'Sabıka Kaydı',
            'cezaYazisi': 'Ceza Yazısı',
            'saglikBeyanFormu': 'Sağlık Beyan Formu',
            'hakemBilgiFormu': 'Hakem Bilgi Formu',


        }
        widgets = {
            'nufusCuzdani': forms.FileInput(attrs={'class': 'form-control'}),
            'diploma': forms.FileInput(attrs={'class': 'form-control'}),
            'sabikaKaydi': forms.FileInput(attrs={'class': 'form-control'}),
            'cezaYazisi': forms.FileInput(attrs={'class': 'form-control'}),
            'saglikBeyanFormu': forms.FileInput(attrs={'class': 'form-control'}),
            'hakemBilgiFormu': forms.FileInput(attrs={'class': 'form-control'}),

        }