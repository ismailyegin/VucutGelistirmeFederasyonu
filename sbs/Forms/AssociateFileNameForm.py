from django import forms
from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.AssociateDegreeFileName import AssociateDegreeFileName


class AssociateFileNameForm(BaseForm):
    class Meta:
        model = AssociateDegreeFileName
        fields = ('name',)
        labels = {'name': 'Doküman İsmi', }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

        }
