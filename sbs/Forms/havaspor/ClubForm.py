from django import forms
from django.forms import ModelForm

from sbs.models.havaspor.Branch import Branch
from sbs.models.havaspor.Club import Club


class ClubForm(ModelForm):
    branch = forms.ModelMultipleChoiceField(queryset=None)
    class Meta:
        model = Club

        fields = (
            'name', 'shortName', 'foundingDate', 'clubMail', 'isFormal', 'branch', 'petition', 'logo',)
        labels = {
            'name': 'Adı',
            'shortName': 'Kısa Adı',
            'foundingDate': 'Kuruluş Tarihi',
            'clubMail': 'Email',
            'isFormal': 'Kulüp Türü',
            'petition': 'Yetki Belgesi',
            'logo': 'Kulüp Logo',
            'branch':'Branş'

        }
        widgets = {
            'isFormal': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; '}),

            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required', "style": "text-transform:uppercase"}),

            # 'shortName': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),

            'clubMail': forms.TextInput(attrs={'class': 'form-control'}),

            'foundingDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),




        }

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['branch'].queryset = Branch.objects.filter(isDeleted=False)
            self.fields['branch'].label = 'Branş *'
            self.fields['branch'].widget.attrs = {'class': 'form-control select2 select2-hidden-accessible',
                                                  'style': 'width: 100%;', 'data-select2-id': '7',
                                                  'data-placeholder': 'Branş Seçin', }
