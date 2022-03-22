from django import forms

from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.ProgressReport import ProgressReport


class ProgressReportForm(BaseForm):
    class Meta:
        model = ProgressReport
        fields = ('definition','reportFile',)
        labels = {'definition': 'Açıklama',
                  'reportFile': 'İlerleme Raporu',
                  }
        widgets = {
            'definition': forms.TextInput(
                attrs={'class': 'form-control '}),

        }