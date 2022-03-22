from django import forms

from sbs.models.ekabis.ConnectionRegion import ConnectionRegion


class YekaConnectionRegionForm(forms.Form):
    connectionRegion = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['connectionRegion'].queryset =ConnectionRegion.objects.filter(isDeleted=False)
        self.fields['connectionRegion'].widget.attrs = {'class': 'select2 select2-hidden-accessible',
                                                             'style': 'width: 100%;', 'data-select2-id': '7',
                                                             'data-placeholder': 'Bağlanti Bölgesi Seçiniz', }


    #ManyToMany -ModelForm
    # class Meta:
    #     model = YekaConnectionRegion
    #     fields = ('connectionRegion',)
    # connectionRegion = forms.ModelMultipleChoiceField(queryset=ConnectionRegion.objects.filter(isDeleted=False))
    #
    # def __init__(self, *args, **kwargs):
    #     if kwargs.get('instance'):
    #         initial = kwargs.setdefault('initial', {})
    #         forms.ModelForm.__init__(self, *args, **kwargs)
    #         initial['connectionRegion'] = [t.pk for t in kwargs['instance'].connectionRegion.all()]
    #         self.fields['connectionRegion'].initial = initial['connectionRegion']
    #
    #     forms.ModelForm.__init__(self, *args, **kwargs)
    #     self.fields['connectionRegion'].widget.attrs = {'class': 'select2 select2-hidden-accessible',
    #                                                     'style': 'width: 100%;', 'data-select2-id': '7',
    #                                                     'data-placeholder': 'Bağlanti Bölgesi Seçiniz', }
