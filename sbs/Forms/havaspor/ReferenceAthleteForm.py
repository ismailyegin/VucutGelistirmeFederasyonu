from django import forms

from sbs.models import ReferenceAthlete
from sbs.models.tvfbf.ReferenceCoach import ReferenceCoach
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models
from sbs.models.ekabis.CategoryItem import CategoryItem


class ReferenceAthleteForm(ModelForm):
    class Meta:
        model = ReferenceAthlete
        fields = (
            'profileImage', 'tc', 'first_name', 'last_name', 'email', 'phoneNumber', 'address', 'phoneNumber2', 'city',
            'country', 'birthDate', 'gender', 'birthplace', 'motherName', 'fatherName', 'iban', 'license_club',
            'licenseNo', 'lisansPhoto', 'expireDate', 'startDate', 'licenseBranch',
            'license_city', 'license_year')

        labels = {'iban': 'İban Adresi', 'first_name': 'Ad', 'last_name': 'Soyad', 'email': 'Email',
                  'phoneNumber': 'Cep Telefonu', 'phoneNumber2': 'Sabit Telefon', 'postalCode': 'Posta Kodu',
                  'city': 'İl', 'country': 'Ülke', 'tc': 'T.C.', 'gender': 'Cinsiyet', 'birthplace': 'Doğum Yeri',
                  'motherName': 'Anne Adı', 'fatherName': 'Baba Adı', 'license_club': 'Kulüp',
                  'lisansPhoto': 'Lisans Fotoğrafı', 'licenseNo': 'Lisans No', 'expireDate': 'Geçerlilik Tarihi',
                  'startDate': 'Lisans Tescil Tarihi', 'license_city': 'Lisans İl', 'licenseBranch': 'Branş',
                  'license_year': 'Sezon'}
        widgets = {

            'tc': forms.TextInput(attrs={'class': 'form-control ' , 'required': 'required','readonly':'readonly'}),

            'birthplace': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required','readonly':'readonly'}),

            'motherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required','readonly':'readonly'}),

            'fatherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required','readonly':'readonly'}),
            'iban': forms.TextInput(
                attrs={'id': 'iban', 'class': 'form-control  iban',
                       'onkeyup': 'if(this.value.length > 34){this.value=this.value.substr(0, 34);}', 'value': '',
                       'required': 'required'}),

            'birthDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'on',
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric",'readonly':'readonly'}),

            'gender': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; ','disabled':'disabled'}),

            'first_name': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required','readonly':'readonly'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required','readonly':'readonly'}),
            'email': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '3'}),

            'phoneNumber': forms.TextInput(attrs={'class': 'form-control '}),

            'phoneNumber2': forms.TextInput(attrs={'class': 'form-control '}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;'}),

            'country': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%;'}),
            'licenseNo': forms.TextInput(
                attrs={'class': 'form-control ','readonly':'readonly'}),
            'license_year': forms.TextInput(
                attrs={'class': 'form-control ','placeholder':'Yıl','readonly':'readonly'}),
            'license_city': forms.TextInput(
                attrs={'class': 'form-control '}),
            'expireDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'on',
                       'onkeydown': 'return true',  "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),
            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'on',
                       'onkeydown': 'return true',  "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),
            'licenseBranch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                 'style': 'width: 100%;', }),
            'license_club': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                'style': 'width: 100%;', }),

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
