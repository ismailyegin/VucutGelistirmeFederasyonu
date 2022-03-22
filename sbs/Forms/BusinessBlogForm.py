from django import forms
from django.forms import ModelForm

from sbs.Forms.BaseForm import BaseForm
from sbs.models.ekabis.BusinessBlog import BusinessBlog


class BusinessBlogForm(BaseForm):
    class Meta:
        model = BusinessBlog
        fields = ('name',
                  'start_notification',
                  'finish_notification',)
        labels = {'name': 'Tanımı',
                  'start_notification':'Başlangıçtan İtibaren Gün',
                  'finish_notification':'Süre Bitiminden Önce Gün'
                  }

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'start_notification':forms.TextInput(attrs={'class': 'form-control ', 'required': 'required','onkeypress':'validate(event)'}),
            'finish_notification':forms.TextInput(attrs={'class': 'form-control ', 'required': 'required','onkeypress':'validate(event)'}),





        }