from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models
from unicode_tr import unicode_tr


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_active')
        labels = {'first_name': 'Ad', 'last_name': 'Soyad', 'email': 'Email'}
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'email': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            'is_active': forms.CheckboxInput(attrs={'class': 'iCheck-helper'}),

        }

    def clean_first_name(self):
        data = unicode_tr(self.cleaned_data['first_name']).upper()
        return data
    def clean_last_name(self):
        data = unicode_tr(self.cleaned_data['last_name']).upper()
        return data

    def clean_email(self):

        data = self.cleaned_data['email']
        print(self.instance)
        if  self.instance.id is None:
            if User.objects.filter(email=data).exists():
                raise forms.ValidationError("Bu email başka bir kullanıcı tarafından kullanılmaktadır.")
            return data
        else:
            return data

    # def save(self, commit=False):
    #     self.first_name=self.cleaned_data['first_name'].upper()
    #     self.last_name=self.cleaned_data['last_name'].upper()
    #     print(self.first_name)
    #     # self.first_name = self.first_name.upper()
    #     # self.last_name = self.last_name.upper()
    #     return ModelForm.save(self, commit=False)




    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
