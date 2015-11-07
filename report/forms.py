
from django import forms
from bootstrap3_datetime.widgets import DateTimePicker

from branchoffice.models import BranchOffice, Car
from staff.models import Employee
from guest.models import Guest

from datetime import datetime

class ReportForm(forms.Form):
    EXPORT_CHOICES = (
        (1, 'Web'),
        (2, 'Excel'),
        (3, 'PDF'),
    )

    REGISTER_CHOICES = (
        (1, 'Entrada de Vehiculos'),
        (2, 'Salida de Vehiculos'),
        (3, 'Ambos registros  de Vehiculos'),
        (4, 'Registro de Vehiculos juntos'),
        (5, 'Registro de personas'),
        (6, 'Registro de ingresos a Taller'),
        (7, 'Todos los conductores de vehiculos'),
        (8, 'Todos los guardias'),
        (9, 'Todos los Vehiculos'),
    )
    export_to = forms.ChoiceField(choices=EXPORT_CHOICES,
                                 widget=forms.Select(attrs={'class': 'form-control',
                                                            'autofocus': ''}))
    registers = forms.ChoiceField(choices=REGISTER_CHOICES,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    branchoffice = forms.ModelChoiceField(queryset=BranchOffice.objects.all(),
                                          widget=forms.Select(attrs={'class': 'form-control'}),
                                          required=False)
    report_date = forms.DateField(widget=DateTimePicker(options={"format":"DD/MM/YYYY", "pickTime": False}),
                                  required=False)
    report_date_start = forms.DateField(widget=DateTimePicker(options={"format":"DD/MM/YYYY", "pickTime": False}),
                                        required=False)
    report_date_end = forms.DateField(widget=DateTimePicker(options={"format":"DD/MM/YYYY", "pickTime": False}),
                                      required=False)
    item_employee = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Item del conductor'}),
                                    required=False)
    item_car = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Interno del Vehiculo'}),
                               required=False)
    ci_guest = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Numero de CI'}),
                                    required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        report_date = self.cleaned_data.get('report_date')
        report_date_start = self.cleaned_data.get('report_date_start')
        report_date_end = self.cleaned_data.get('report_date_end')
        registers = self.cleaned_data.get('registers')

        if registers == '7' or registers == '8' or registers == '9':
            return cleaned_data

        if not report_date and not report_date_start and not report_date_end:
            raise forms.ValidationError('Tiene que seleccionar alguna fecha o intervalo')
        elif report_date_start and not report_date_end:
            raise forms.ValidationError('Si marca una fecha de inicio tiene que ' +
                                        'especificar una fecha fin')
        elif not report_date_start and report_date_end:
            raise forms.ValidationError('Tiene que seleccionar una fecha de inicio')
        else:
            return cleaned_data

    def clean_report_date(self):
        report_date = self.cleaned_data['report_date']
        today = datetime.today().date()

        if report_date:
            if report_date > today:
                raise forms.ValidationError('La fecha que selecciono es mayor a la fecha actual')
            else:
                return report_date
        else:
            return report_date

    def clean_report_date_start(self):
        report_date_start = self.cleaned_data['report_date_start']
        today = datetime.today().date()

        if report_date_start:
            if report_date_start > today:
                raise forms.ValidationError('La fecha que selecciono es mayor a la fecha actual')
            else:
                return report_date_start
        else:
            return report_date_start

    def clean_item_employee(self):
        item = self.cleaned_data['item_employee']
        if not item:
            return item
        else:
            try:
                employee = Employee.objects.get(item=item)
                return employee
            except Employee.DoesNotExist:
                raise forms.ValidationError('El conductor no existe')

    def clean_item_car(self):
        item_car = self.cleaned_data['item_car']
        if not item_car:
            return item_car
        else:
            try:
                car = Car.objects.get(internal_number=item_car)
                return car
            except Car.DoesNotExist:
                raise forms.ValidationError('El Vehiculo no existe')

    def clean_ci_guest(self):
        ci = self.cleaned_data['ci_guest']
        if not ci:
            return ci
        else:
            try:
                g = Guest.objects.get(val_document=ci)
                return g.val_document
            except Guest.DoesNotExist:
                raise forms.ValidationError('Este CI no existe: ' + ci)

