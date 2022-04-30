from django import forms
from django.forms import ModelForm

from sbs.models.tvfbf.SportFacility import SportFacility


class SportFacilityForm(ModelForm):
    class Meta:
        model = SportFacility

        fields = (
            'name', 'derbis', 'mersis', 'permitDate', 'coordinate', 'registrationNumber', 'status')

        labels = {'name': 'Özel Spor Tesisi Adı', 'derbis': 'Derbis No', 'mersis': 'Mersis No',
                  'permitDate': 'Çalışma İzin Bel.Ver.Tar.', 'coordinate': 'Koordinat',
                  'registrationNumber': 'İşyeri Tescil No', 'status': 'Tesis Durumu'}

        widgets = {

            'permitDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask2013', 'id': 'datepicker', 'autocomplete': 'on',
                      }),
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'derbis': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'mersis': forms.TextInput(attrs={'class': 'form-control', }),
            'coordinate': forms.TextInput(attrs={'class': 'form-control', }),
            'registrationNumber': forms.TextInput(attrs={'class': 'form-control', }),
            'status': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                   'style': 'width: 100%; '}),
        }
