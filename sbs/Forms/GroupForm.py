from django import forms
from django.contrib.auth.models import Group

from sbs.Forms.BaseForm import BaseForm


class GroupForm(BaseForm):
    class Meta:
        model = Group
        fields = ('name',)
        labels = {'name': 'İsim '}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
        }