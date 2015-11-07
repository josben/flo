
from django import forms
from bootstrap3_datetime.widgets import DateTimePicker

from branchoffice.models import Car
from maintenance.models import Workshop

import datetime

class FormMaintenanceProgram(forms.Form):
    workshop = forms.ModelChoiceField(queryset=Workshop.objects.filter(is_active=True),
                                      widget=forms.Select(attrs={'class': 'form-control'}),
                                      initial=0)
    internal_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'Interno del Vehiculo',
                                                                    'onchange': 'maintenance_car()',
                                                                    'autofocus':''}))
    next_km_maintenance = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Kilometraje'}),
                                             required=False)
    next_date_maintenance = forms.DateField(widget=DateTimePicker(options={"format":"DD/MM/YYYY", "pickTime": False}))
    reason = forms.CharField(widget=forms.Textarea(attrs={'rows': '3',
                                                          'class': 'form-control',
                                                          'placeholder': 'Motivo del mantenimiento'}),
                             required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        internal_number = self.cleaned_data.get('internal_number')
        km = self.cleaned_data.get('next_km_maintenance')
        try:
            car = Car.objects.get(internal_number=internal_number)
        except Car.DoesNotExist:
            raise forms.ValidationError('El Vehiculo no existe')
        if car.current_km:
            if km < car.current_km:
                raise forms.ValidationError('El Kilometraje es menor que su km actual.')
            else:
                return cleaned_data
        else:
            return cleaned_data

    def clean_internal_number(self):
        internal_number = self.cleaned_data['internal_number']
        try:
            car = Car.objects.get(internal_number=internal_number)
            return car.internal_number
        except Car.DoesNotExist:
            return forms.ValidationError('El interno del Vehiculo no existe')

    def clean_next_date_maintenance(self):
        next_date_maintenance = self.cleaned_data['next_date_maintenance']
        if next_date_maintenance < datetime.date.today():
            raise forms.ValidationError('La fecha debe ser mayor la de hoy')
        else:
            return next_date_maintenance

class FormWorkshop(forms.ModelForm):
    class Meta:
        model = Workshop
        widgets = {
                'branchoffice': forms.Select(attrs={'class': 'form-control',
                                                    'autofocus': ''}),
                'description': forms.Textarea(attrs={'rows': '3',
                                                     'class': 'form-control',
                                                     'placeholder': 'Ingrese alguna descripcion'})
        }

    def clean_branchoffice(self):
        branchoffice = self.cleaned_data['branchoffice']
        try:
            bo = Workshop.objects.get(branchoffice=branchoffice)
            raise forms.ValidationError('El taller %s ya existe' % bo.branchoffice)
        except Workshop.DoesNotExist:
            return branchoffice

