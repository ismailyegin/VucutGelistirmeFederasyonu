from django import forms
from django.forms import ModelForm

from sbs.models.tvfbf.Branch import Branch
from sbs.models.tvfbf.Club import Club


class TransClubForm(ModelForm):
    # branch = forms.ModelMultipleChoiceField(queryset=None)
    class Meta:
        model = Club

        fields = (
            'name', 'foundingDate', 'clubMail','derbis',)
        labels = {
            'name': 'Adı',
            'foundingDate': 'Kuruluş Tarihi',
            'clubMail': 'Email',


        }
        widgets = {

            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required', "style": "text-transform:uppercase",'readonly':'readonly'}),

            'clubMail': forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
            'derbis': forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
            'foundingDate': forms.TextInput(
                attrs={'class': 'form-control','readonly':'readonly'}),




        }

    # def __init__(self, *args, **kwargs):
    #         super().__init__(*args, **kwargs)
    #         self.fields['branch'].queryset = Branch.objects.filter(isDeleted=False)
    #         self.fields['branch'].label = 'Branş *'
    #         self.fields['branch'].widget.attrs = {'class': 'form-control select2 select2-hidden-accessible',
    #                                               'style': 'width: 100%;', 'data-select2-id': '7',
    #                                               'data-placeholder': 'Branş Seçin', }
