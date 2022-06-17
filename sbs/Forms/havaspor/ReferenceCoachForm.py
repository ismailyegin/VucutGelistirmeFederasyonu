# -*- coding: utf-8 -*-

from django import forms

from sbs.models.ekabis.Country import Country
from sbs.models.tvfbf.ReferenceCoach import ReferenceCoach
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models
from sbs.models.ekabis.CategoryItem import CategoryItem


class RefereeCoachForm(ModelForm):
    kademe_definition = forms.ModelChoiceField(queryset=CategoryItem.objects.filter(forWhichClazz='COACH_GRADE'),
                                               to_field_name='name',
                                               empty_label="Seçiniz",
                                               label="Kademe",
                                               required='required',
                                               widget=forms.Select(
                                                   attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                          'style': 'width: 100%; '}))

    country = forms.ModelChoiceField(queryset=Country.objects.order_by('-order'),
                                               to_field_name='name',
                                               empty_label="Seçiniz",
                                               label="Ülke",
                                               required='required',
                                               widget=forms.Select(
                                                   attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                          'style': 'width: 100%; '}))


    class Meta:
        model = ReferenceCoach
        fields = (
            'first_name', 'last_name', 'email', 'phoneNumber', 'address', 'postalCode', 'phoneNumber2', 'city',
            'country', 'iban', 'tc', 'profileImage', 'birthDate', 'gender', 'birthplace', 'motherName',
        'fatherName','kademe_belge','kademe_startDate','sgk','dekont','belge')



        labels = {'iban': 'İban Adresi', 'first_name': 'Ad', 'last_name': 'Soyad', 'email': 'Email',
                  'phoneNumber': 'Cep Telefonu', 'phoneNumber2': 'Sabit Telefon', 'postalCode': 'Posta Kodu',
                  'city': 'İl', 'country': 'Ülke', 'tc': 'T.C.', 'gender': 'Cinsiyet','kademe_belge':'Antrenör Sözleşme Belgesi: ',
                  'kademe_startDate':'Kademe Başlangıç Zamanı ','sgk':'SGK/Bağ-Kur Belgesi: ','dekont':'Vize Dekont','belge':'Antrenör Belgesi'}
        widgets = {

            'tc': forms.TextInput(attrs={'class': 'form-control ',
                                            'onkeyup': 'if(this.value.length >11){this.value=this.value.substr(0, 11);}',
                                            'id': 'tc',
                                          'onkeypress':'return isNumberKey(event)',
                                            'value': '',
                                            'required': 'required'}),

            'birthplace': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),

            'motherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),

            'fatherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),
            'iban': forms.TextInput(
                attrs={'id':'iban','class': 'form-control  iban','onkeyup':'if(this.value.length > 34){this.value=this.value.substr(0, 34);}','value': '', 'required': 'required'}),

             'birthDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'on',
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),

            'gender': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

            'first_name': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'email': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '2'}),

            'phoneNumber': forms.TextInput(attrs={'class': 'form-control '}),

            'phoneNumber2': forms.TextInput(attrs={'class': 'form-control '}),

            'postalCode': forms.TextInput(attrs={'class': 'form-control '}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),
            'kademe_startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'on',
                       'onkeydown': 'return true',"data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),

        }

    def clean_email(self):

        data = self.cleaned_data['email']
        print(self.instance)
        if self.instance.id is None:
            if User.objects.filter(email=data).exists():
                raise forms.ValidationError("Bu email başka bir kullanıcı tarafından kullanılmaktadır.")
            return data
        else:
            return data

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
