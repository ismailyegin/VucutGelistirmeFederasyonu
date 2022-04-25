from django import forms
from django.forms import ModelForm

from sbs.models.tvfbf.Branch import Branch
from sbs.models.tvfbf.SportFacilityManager import SportFacilityManager


class SportFacilityManagerForm(ModelForm):
    branch = forms.ModelMultipleChoiceField(queryset=None)

    class Meta:
        model = SportFacilityManager

        fields = (
             'personalityType',)

        labels = {'personalityType': 'Tesis Kişilik Türü', }

        widgets = {


            'personalityType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].queryset = Branch.objects.filter(isDeleted=False)
        self.fields['branch'].label = 'Branş *'
        self.fields['branch'].widget.attrs = {'class': 'form-control select2 select2-hidden-accessible',
                                                        'style': 'width: 100%;',
                                                         }