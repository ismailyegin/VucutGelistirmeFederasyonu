from django import forms
from django.forms import ModelForm
from sbs.models.ekabis.CategoryItem import CategoryItem
from sbs.models.tvfbf.ReferenceClub import ReferenceClub

from sbs.models.tvfbf.PreRegistration import PreRegistration


class ReferenceClubUpdateForm(ModelForm):
    kademe_definition = forms.ModelChoiceField(queryset=CategoryItem.objects.filter(forWhichClazz='COACH_GRADE'),
                                               to_field_name='name',
                                               empty_label="Seçiniz",
                                               required=False,
                                               label="Kademe",
                                               widget=forms.Select(
                                                   attrs={'class': 'form-control select2 ',
                                                          'style': 'width: 100%; '}))

    class Meta:
        model = ReferenceClub

        fields = (
            'tc', 'profileImage',  'birthDate', 'bloodType', 'gender', 'birthplace', 'motherName',
            'fatherName', 'first_name', 'last_name', 'email', 'is_active', 'phoneNumber', 'address',
            'phoneNumber2', 'city', 'country', 'name', 'shortName', 'foundingDate', 'logo', 'clubMail',
            'clubphoneNumber', 'clubaddress', 'clubpostalCode', 'clubphoneNumber2', 'clubcity', 'clubcountry',
            'clubFax', 'clubTown',
             'role', 'isCoach', 'kademe_belge', 'kademe_startDate', 'iban', 'kademe_definition', 'derbis')
        labels = {'tc': 'T.C.', 'gender': 'Cinsiyet', 'first_name': 'Ad', 'last_name': 'Soyad', 'email': 'Email',
                  'phoneNumber': 'Cep Telefonu', 'derbis': 'Derbis Kütük No', 'clubTown': 'İlçe',
                  'clubFax': 'Faks',
                  'phoneNumber2': 'Sabit Telefon', 'postalCode': 'Posta Kodu', 'city': 'İl', 'country': 'Ülke',
                  'name': 'Adı', 'shortName': 'Kısa Adı',
                  'foundingDate': 'Kuruluş Tarihi', 'clubMail': 'Email', 'isFormal': 'Kulüp Türü', 'role': 'Kulüp Rolü',
                  'clubphoneNumber': 'Cep Telefonu', 'clubphoneNumber2': 'Sabit Telefon',
                  'isCoach': 'Aynı zaman da kulüp Antrenörü müsünüz?',
                  'kademe_belge': 'Antrenörlük Belgesi Yükleyiniz: ', 'kademe_startDate': 'Kademe Başlangıç Zamanı ',
                  'iban': 'iban adresini giriniz'}

        widgets = {

            'iban': forms.TextInput(
                attrs={'id': 'iban', 'class': 'form-control  iban',
                       'onkeyup': 'if(this.value.length > 34){this.value=this.value.substr(0, 34);}', 'value': ''}),

            'kademe_startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker4', 'autocomplete': 'off',
                       'onkeydown': 'return true', }),

            'isCoach': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%; ', 'required': 'required'}),

            'role': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%; ', 'required': 'required'}),

            'shortName': forms.TextInput(attrs={'class': 'form-control',}),

            'clubaddress': forms.Textarea(attrs={'class': 'form-control ', 'rows': '3',}),

            'clubphoneNumber': forms.TextInput(attrs={'class': 'form-control ',}),

            'clubphoneNumber2': forms.TextInput(attrs={'class': 'form-control '}),

            'clubpostalCode': forms.TextInput(attrs={'class': 'form-control '}),
            'clubcity': forms.TextInput(attrs={'class': 'form-control ',}),


            'clubcountry': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible', 'style': 'width: 100%;',
                       'required': 'required'}),

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '2', 'cols': '5'}),

            'phoneNumber': forms.TextInput(attrs={'class': 'form-control '}),
            'clubFax': forms.TextInput(attrs={'class': 'form-control ',}),

            'clubTown': forms.TextInput(attrs={'class': 'form-control ',}),
            'phoneNumber2': forms.TextInput(attrs={'class': 'form-control '}),

            'postalCode': forms.TextInput(attrs={'class': 'form-control '}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),

            'country': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%;', 'required': 'required'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'email': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            'is_active': forms.CheckboxInput(attrs={'class': 'iCheck-helper'}),

            'tc': forms.TextInput(attrs={'class': 'form-control ',
                                         'onkeyup': 'if(this.value.length >11){this.value=this.value.substr(0, 11);}',
                                         'id': 'tc',
                                         'onkeypress': 'return isNumberKey(event)',

                                         'value': '',
                                         'required': 'required'}),

            'height': forms.TextInput(attrs={'class': 'form-control'}),

            'weight': forms.TextInput(attrs={'class': 'form-control'}),

            'birthplace': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),

            'motherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),

            'fatherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),

            'birthDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),

            'bloodType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%; '}),

            'gender': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required', "style": "text-transform:uppercase",
                       }),

            'clubMail': forms.TextInput(attrs={'class': 'form-control',}),
            'derbis': forms.TextInput(attrs={'class': 'form-control', }),
            'foundingDate': forms.TextInput(
                attrs={'class': 'form-control', }),

        }
