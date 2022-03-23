from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm


class RefereeUserForm(ModelForm):
    class Meta:
        model = User

        fields = ('first_name', 'last_name', 'email',)
        labels = {
            'first_name': 'İsim',
            'last_name': 'Soyisim',
            'email': 'Email',

        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}),
        }
