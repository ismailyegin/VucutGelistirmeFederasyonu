from django import forms
from django.forms import ModelForm
from sbs.models.tvfbf.SportFacility import SportFacility


class FacilitySearchForm(ModelForm):

    class Meta:
        model = SportFacility
        fields = ('name', 'derbis',)
        labels = {'name': 'Tesis Adı', 'derbis': 'Derbis No'}
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': ' TESİS ADI', 'value': '', "style": "text-transform:uppercase"
                       }),
            'derbis': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': ' DERBİS NO', "style": "text-transform:uppercase"}),

        }


