from django import forms
from django.forms import ModelForm

from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.CompanyUser import CompanyUser


class CompanyUserForm(BaseForm):
    class Meta:
        model = CompanyUser
        fields = (
            'authorization_period_start',
            'authorization_period_finish',

        )
        labels = {'authorization_period_start': 'Kullanıcı Yetki Başlangıç Zamanı *',
                  'authorization_period_finish': 'Kullanıcı Yetki Bitiş Zamanı *',
                  }
        widgets = {
            'authorization_period_finish': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),
            'authorization_period_start': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker2', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),
        }
