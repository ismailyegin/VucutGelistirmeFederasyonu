from django import forms
from django.forms import ModelForm
from sbs.models.ekabis.Person import Person


class SportFacilityManagerPersonForm(ModelForm):
    class Meta:
        model = Person

        fields = (
            'profileImage', 'tc' )

        labels = {'tc': 'T.C*.',
                  'profileImage': 'Profil Resmi',


                  }

        widgets = {

            'profileImage': forms.FileInput(),
            'tc': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required', 'onkeypress': 'validate(event)',
                       'onkeyup': 'if(this.value.length >11){this.value=this.value.substr(0, 11);}',
                       'placeholder': ""}),


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
