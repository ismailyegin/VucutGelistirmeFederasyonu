from django import forms
from django.forms import ModelForm
from sbs.models.tvfbf.Announcement import Announcement


class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement

        fields = ('title', 'text', 'group', 'startDate', 'finishDate',)

        labels = {'title': 'Duyuru Başlığı',
                  'text': 'Duyuru İçeriği',
                  'group': 'Duyurunun Gözükeceği Gruplar',
                  'startDate': 'Duyuru Balangıç Tarihi',
                  'finishDate': 'Duyuru Bitiş Tarihi',
                  }

        widgets = {

            'title': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'required'}),

            'group': forms.SelectMultiple(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                 'style': 'width: 100%;', 'required': 'required'}),

            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker', 'autocomplete': 'off',
                       'required': 'required'}),

            'finishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker4', 'autocomplete': 'off',
                       'required': 'required'}),

        }
