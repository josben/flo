
from django import forms

from company.models import Company

class CompanyForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Nombre'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Direccion'}),
                              required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                               'rows': '3',
                                                               'placeholder': 'Descripcion'}),
                                  required=False)

    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            c = Company.objects.get(name=name)
            raise forms.ValidationError('La oficina ya existe: %s' % c.name)
        except Company.DoesNotExist:
            return name

