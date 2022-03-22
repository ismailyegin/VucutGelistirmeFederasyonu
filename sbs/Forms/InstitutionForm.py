from django import forms
from sbs.models.ekabis.Institution import Institution
from sbs.Forms.BaseForm import BaseForm

class InstitutionForm(BaseForm):
    class Meta:
        model = Institution
        fields = ('name',)
        labels = {
            'name': 'Kurum İsmi',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ',}),



        }
