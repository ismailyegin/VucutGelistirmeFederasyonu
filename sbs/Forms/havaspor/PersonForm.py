from django import forms
from django.forms import ModelForm
from sbs.models import Person


class PersonForm(ModelForm):
    class Meta:
        model = Person

        fields = (
            'tc', 'profileImage',
            'height', 'weight',
            'birthDate', 'bloodType',
            'gender', 'birthplace',
            'motherName',
            'profileImage', 'fatherName',
            'is_unvani', 'hesKodu')

        labels = {'tc': 'T.C*.',
                  'gender': 'Cinsiyet*',
                  'profileImage': 'Profil Resmi',
                  'is_unvani': 'İs Unvanı ',
                  'height': 'Boy',
                  'weight': 'Kilo',
                  'birthplace': 'Doğum Yeri',
                  'birthDate': 'Doğum Tarihi',
                  'motherName': 'Anne Adı',
                  'fatherName': 'Baba Adı',
                  'hesKodu': 'HES Kodu',

                  }

        widgets = {

            'profileImage': forms.FileInput(),

            'is_unvani': forms.TextInput(attrs={'class': 'form-control ', "style": "text-transform:uppercase"}),

            'tc': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required', 'onkeypress': 'validate(event)',
                       'onkeyup': 'if(this.value.length >11){this.value=this.value.substr(0, 11);}',
                       'placeholder': ""}),

            'height': forms.TextInput(attrs={'class': 'form-control', 'onkeypress': 'validate(event)'}),

            'weight': forms.TextInput(attrs={'class': 'form-control', 'onkeypress': 'validate(event)'}),

            'birthplace': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', "style": "text-transform:uppercase"}),

            'motherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', "style": "text-transform:uppercase"}),

            'fatherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', "style": "text-transform:uppercase"}),

            'birthDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker', 'autocomplete': 'off',
                       'required': 'required'}),

            'bloodType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%;'}),

            'gender': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%;', 'required': 'required'}),
            'hesKodu': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', "style": "text-transform:uppercase"}),

        }

    def clean_tc(self):

        data = self.cleaned_data['tc']
        print(self.instance)
        if self.instance is None:
            if Person.objects.filter(tc=data).exists():
                raise forms.ValidationError("This tc already used")
            return data
        else:
            return data
