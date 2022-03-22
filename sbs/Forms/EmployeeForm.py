from django import forms
from django.forms import ModelForm

from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.Employee import Employee


class EmployeeForm(BaseForm):
    class Meta:
        model = Employee

        fields = ()
        labels = {}


