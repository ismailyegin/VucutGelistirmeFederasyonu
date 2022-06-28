from django import forms
from django.forms import ModelForm

from sbs.models import Country
from sbs.models.ekabis.CategoryItem import CategoryItem
from sbs.models.tvfbf.ReferenceReferee import ReferenceReferee


class PreRefereeForm(ModelForm):
    kademe_definition = forms.ModelChoiceField(
        queryset=CategoryItem.objects.filter(forWhichClazz='REFEREE_GRADE', isDeleted=False).order_by('order'),
        to_field_name='name',
        empty_label="Seçiniz",
        label="Kokart",
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
        model = ReferenceReferee
        fields = (
            'first_name', 'last_name', 'email', 'phoneNumber', 'address', 'phoneNumber2',
            'city', 'grade_referee_contract', 'tc', 'profileImage', 'birthDate', 'iban',
            'gender', 'birthplace', 'motherName', 'fatherName', 'referee_file', 'sgk', 'dekont', 'gradeDate')
        labels = {'first_name': 'Ad', 'last_name': 'Soyad', 'email': 'Email', 'phoneNumber': 'Cep Telefonu',
                  'phoneNumber2': 'Sabit Telefon', 'city': 'İl', 'tc': 'T.C.', 'gender': 'Cinsiyet',
                  'referee_file': 'Hakem Belgesi', 'grade_referee_contract': 'Hakem Sözleşme Belgesi',
                  'sgk': 'SGK/Bağ-Kur Belgesi', 'dekont': 'Vize Dekont', 'gradeDate': 'Hak Kazanma Tarihi'}
        widgets = {

            'profileImage': forms.FileInput(),

            'tc': forms.TextInput(attrs={'class': 'form-control ',
                                         'onkeyup': 'if(this.value.length >11){this.value=this.value.substr(0, 11);}',
                                         'id': 'tc',
                                         'onkeypress': 'return isNumberKey(event)',

                                         'value': '',
                                         'required': 'required'}),

            'birthplace': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),

            'motherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': ''}),

            'fatherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': ''}),

            'birthDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'on',
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),

            'iban': forms.TextInput(attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),

            'gender': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

            'first_name': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'email': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '5', 'required': 'required'}),

            'phoneNumber': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            'phoneNumber2': forms.TextInput(attrs={'class': 'form-control '}),

            'postalCode': forms.TextInput(attrs={'class': 'form-control '}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),

            'gradeDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'on',
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),
        }
