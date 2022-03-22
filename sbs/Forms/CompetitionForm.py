from django import forms
from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.Competition import Competition



class CompetitionForm(BaseForm):

    class Meta:
        model = Competition
        fields = (
            'date',
            'report',

        )
        labels = {'report': 'Yarışma Tutanağı',
                  'date': 'Yarışma Zamanı',
                  }
        widgets = {
            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),
        }
