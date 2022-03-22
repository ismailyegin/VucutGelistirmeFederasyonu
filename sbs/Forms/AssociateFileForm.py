from django import forms

from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.AssociateDegreeFile import AssociateDegreeFile
from sbs.models.ekabis.AssociateDegreeFileName import AssociateDegreeFileName


class AssociateFileForm(BaseForm):
    class Meta:
        model = AssociateDegreeFile
        fields = ('name', 'date', 'file')
        labels = {'file': 'Doküman', 'name': 'Doküman Kategori', 'date': 'Doküman Tarihi'}
        widgets = {
            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),
            'name': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),

        }

    def __init__(self, *args, **kwargs):
        super(AssociateFileForm, self).__init__(*args, **kwargs)
        # access object through self.instance...
        self.fields['name'].queryset = AssociateDegreeFileName.objects.filter(isDeleted=False)
