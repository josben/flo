
from django import forms
from django.core.exceptions import ValidationError

from .models import CarRegistration, AllCarRegistration, StatusCar
from branchoffice.models import Car
from staff.models import Employee
from maintenance.models import Workshop
from utils.utils import DOCUMENT_CHOICES, ISSUE_CHOICES, GENDER_CHOICES
from bootstrap3_datetime.widgets import DateTimePicker

import datetime

class CarRegistrationForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super (CarRegistrationForm,self).__init__(*args,**kwargs)
        if 'stick_date' in request.session:
            aux_date = datetime.datetime.strptime(request.session['stick_date'], '%Y-%m-%d').date()
            initial_date = aux_date.strftime('%d/%m/%Y')
        else:
            initial_date = datetime.datetime.today().date().strftime('%d/%m/%Y')
        self.fields['register_date'] = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'onchange': 'delete_date_session()',
                                                                  'autocomplete': 'off',
                                                                  'data-date-format': "DD/MM/YYYY"}),
                                                       initial=initial_date,
                                                       required=False)

    employee = forms.IntegerField(label='Empleado',
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'autocomplete': 'off',
                                                                'required': 'True',
                                                                'placeholder': 'Item del conductor',
                                                                'width': '100'}))
    integra = forms.BooleanField(required=False)
    car = forms.CharField(label='Vehiculo',
                             widget=forms.TextInput(attrs={'onchange': 'validation_car()',
                                                           'autocomplete': 'off',
                                                           'class': 'form-control',
                                                           'required': 'True',
                                                           'placeholder': 'Interno del Vehiculo',
                                                           'autofocus': ''}))
#    branchoffice = forms.ModelChoiceField(queryset=BranchOffice.objects.all(),
#                                          label='Edificio', required=False)
#    register_date = forms.DateField(widget=DateTimePicker(options={"format":"DD/MM/YYYY",
#                                                                   "pickTime": False},
#                                                                   attrs={'class': 'form-control',
#                                                                          'onchange': 'delete_date_session()'}),
#                                    initial=datetime.date.today(),
#                                    required=False)
    time = forms.TimeField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'data-date-format': 'HH:mm',
                                                         'required': 'True',
                                                         'autocomplete': 'off'}),
                           initial=datetime.datetime.today().time().strftime('%H:%M'))
    km = forms.IntegerField(label='Kilometraje',
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'onchange': 'validation_km()',
                                                          'required': 'True',
                                                          'placeholder': 'Kilometraje',
                                                          'autocomplete': 'off'}))
    ladders = forms.CharField(required=False, label='Escaleras',
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Escaleras',
                                                            'autocomplete': 'off'}))
    observation = forms.CharField(required=False,
                                  max_length=450,
                                  widget=forms.Textarea(attrs={'class': 'form-control',
                                                               'rows': '3'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        car = self.cleaned_data.get('car')
        if car is None:
            raise forms.ValidationError('El interno del auto no existe')
        register_date = self.cleaned_data.get('register_date')
        time = self.cleaned_data.get('time')

        last_register = StatusCar.objects.get(car=car)
        current_time = datetime.datetime.combine(register_date,time)
        if last_register.last_register_car is not None:
            last_time = last_register.last_register_car.register_time
        else:
            last_time = current_time
        if last_time > current_time:
            raise forms.ValidationError('Los datos de fecha y hora que ingreso ' +
                                        current_time.strftime('%d/%m/%Y %H:%M') +
                                        ' es menor a la ultima salida ' + 
                                        last_time.strftime('%d/%m/%Y %H:%M'))
        else:
            return cleaned_data

    def clean_car(self):
        car = self.cleaned_data['car']
        integra = self.cleaned_data['integra']
        try:
            if integra:
                car = 'I-' + str(car)
            car = Car.objects.get(internal_number=car)
            return car
        except Car.DoesNotExist:
            raise forms.ValidationError('El interno del vehiculo NO EXISTE!!')

    def clean_employee(self):
        employee = self.cleaned_data['employee']
        try:
            employee = Employee.objects.get(item=employee)
            return employee
        except Employee.DoesNotExist:
            raise forms.ValidationError('El item ingresado NO EXISTE')

    def clean_observation(self):
        observation = self.cleaned_data['observation']
        if observation:
            return observation
        else:
            return ''

"""
    def clean_km(self):
        car = self.cleaned_data['car']
        km = self.cleaned_data['km']
        status_car = StatusCar.objects.get(car=car)
        if status_car.in_moving:
            if km < car.current_km:
                raise forms.ValidationError('El kilometraje es incorrecto')
            else:
                return km
        else:
            return km
"""

class GuestForm(forms.Form):
    type_document = forms.CharField(required=True,
                                    widget=forms.Select(choices=DOCUMENT_CHOICES,
                                                        attrs={'class': 'form-control'}))
    val_document = forms.CharField(required=True,
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'autofocus': ''}))
    city = forms.CharField(required=True,
                           widget=forms.Select(choices=ISSUE_CHOICES,
                                               attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.CharField(required=True,
                             widget=forms.Select(choices=GENDER_CHOICES,
                                                 attrs={'class': 'form-control'}))
    reason = forms.CharField(required=True,
                             max_length=450,
                             widget=forms.Textarea(attrs={'class': 'form-control',
                                                          'rows': '3'}))

class GuestSimplifiedForm(forms.Form):
    val_document = forms.CharField(required=True,
                                   widget=forms.TextInput(attrs={'onchange': 'searchGuest()',
                                                                 'autocomplete': 'off',
                                                                 'class': 'form-control',
                                                                 'required': 'True',
                                                                 'autofocus': ''}))
    reason = forms.CharField(required=True,
                             max_length=450,
                             widget=forms.Textarea(attrs={'class': 'form-control',
                                                          'required': 'True',
                                                          'rows': '3'}))

class CarRegistrationEditForm(forms.ModelForm):
    register = forms.CharField(required=True, max_length=15)
    employee = forms.CharField(required=True, max_length=15)
    class Meta:
        model = CarRegistration
        fields = ('register_time', 'register_km', 'ladders', 'observation', 'employee', 'register_date')
        widgets = {
                'register_time': DateTimePicker(options={"format":"DD/MM/YYYY HH:mm", "pickTime": True}),
                'register_date': DateTimePicker(options={"format":"DD/MM/YYYY", "pickTime": False}),
                'observation': forms.Textarea(attrs={'rows': '3',
                                                     'class': 'form-control',
                                                     'placeholder': 'Ingrese alguna observacion'}),
                'ladders': forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': 'Escaleras'}),
                'register_km': forms.TextInput(attrs={'class': 'form-control',
                                                      'required': 'True',
                                                      'placeholder': 'Kilometraje'})
        }

    def clean_employee(self):
        value = self.cleaned_data['employee']
        try:
            employee = Employee.objects.get(item=value)
        except Employee.DoesNotExist:
            raise ValidationError('El item no existe')
        return employee

    def clean(self):
        cleaned_data = self.cleaned_data
        form_register_id = self.cleaned_data.get('register')
        employee = self.cleaned_data.get('employee')
        form_register_date = self.cleaned_data.get('register_date')
        form_register_time = self.cleaned_data.get('register_time')
        form_register_km = self.cleaned_data.get('register_km')
        form_ladders = self.cleaned_data.get('ladders')
        form_register_obs = self.cleaned_data.get('observation')

        if not employee:
            raise ValidationError("El item ingresado del conductor no existe")

        if form_register_date != form_register_time.date():
            raise ValidationError("Las dos fechas deben ser iguales")

        register = CarRegistration.objects.get(id=form_register_id)
        if register.event == 'entrada':
            try:
                reg_all_row = AllCarRegistration.objects.get(register_in=register)
                if reg_all_row.km_in != form_register_km:
                    if reg_all_row.km_out > form_register_km:
                        raise ValidationError("ERROR: El Kilometraje el menor que su salida")
                    reg_all_row.km_in = form_register_km
                    reg_all_row.save()
                    register.register_km = form_register_km
                    register.save()
                if reg_all_row.time_in != form_register_time:
                    reg_all_row.time_in = form_register_time
                    reg_all_row.register_date = form_register_date
                    reg_all_row.save()
                    register.register_date = form_register_date
                    register.register_time = form_register_time
                    register.save()
                if reg_all_row.ladders_in != form_ladders:
                    reg_all_row.ladders_in = form_ladders
                    reg_all_row.save()
                    register.ladders = form_ladders
                    register.save()
                if reg_all_row.custody_in != employee:
                    reg_all_row.custody_in = employee
                    reg_all_row.save()
                    register.employee = employee
                    register.save()
            except AllCarRegistration.DoesNotExist:
                if register.register_km != form_register_km:
                    register.register_km = form_register_km
                    register.save()
                if register.register_time != form_register_time:
                    register.register_date = form_register_date
                    register.register_time = form_register_time
                    register.save()
                if register.ladders != form_ladders:
                    register.ladders = form_ladders
                    register.save()
                if register.employee != employee:
                    register.employee = employee
                    register.save()
        else:
            try:
                reg_all_row = AllCarRegistration.objects.get(register_out=register)
                if reg_all_row.km_out != form_register_km:
                    if form_register_km > reg_all_row.km_in:
                        raise ValidationError("ERROR: El Kilometraje de salida ingresado " +
                                              "es mayor que su km de ingreso registrado")
                    reg_all_row.km_out = form_register_km
                    reg_all_row.save()
                    register.register_km = form_register_km
                    register.save()
                if reg_all_row.time_out != form_register_time:
                    reg_all_row.time_out = form_register_time
                    reg_all_row.save()
                    register.register_date = form_register_date
                    register.register_time = form_register_time
                    register.save()
                if reg_all_row.ladders_out != form_ladders:
                    reg_all_row.ladders_out = form_ladders
                    reg_all_row.save()
                    register.ladders = form_ladders
                    register.save()
                if reg_all_row.custody_out != employee:
                    reg_all_row.custody_out = employee
                    reg_all_row.save()
                    register.employee = employee
                    register.save()
            except AllCarRegistration.DoesNotExist:
                if register.register_time != form_register_time:
                    register.register_time = form_register_time
                    register.register_date = form_register_date
                    register.save()
                if register.register_km != form_register_km:
                    register.register_km = form_register_km
                    register.save()
                if register.ladders != form_ladders:
                    register.ladders = form_ladders
                    register.save()
                if register.employee != employee:
                    register.employee = employee
                    register.save()
        if register.observation != form_register_obs:
            register.observation = form_register_obs
            register.save()

        return cleaned_data

class ForeignCarRegistrationForm(forms.Form):
    TYPE_EVENT = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida')
    )
    event = forms.ChoiceField(choices=TYPE_EVENT,
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    employee = forms.IntegerField(label='Empleado',
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'autocomplete': 'off',
                                                                'required': 'True',
                                                                'placeholder': 'Item del conductor',
                                                                'width': '100'}))
    integra = forms.BooleanField(required=False)
    car = forms.CharField(label='Vehiculo',
                          widget=forms.TextInput(attrs={'autocomplete': 'off',
                                                        'class': 'form-control',
                                                        'required': 'True',
                                                        'placeholder': 'Interno del Vehiculo',
                                                        'autofocus': ''}))
    register_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'onchange': 'delete_date_session()',
                                                                  'autocomplete': 'off',
                                                                  'data-date-format': "DD/MM/YYYY"}),
                                    initial=datetime.datetime.today().date().strftime('%d/%m/%Y'),
                                    required=False)
    time = forms.TimeField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'data-date-format': 'HH:mm',
                                                         'required': 'True',
                                                         'autocomplete': 'off'}),
                           initial=datetime.datetime.today().time().strftime('%H:%M'))
    km = forms.IntegerField(label='Kilometraje',
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Kilometraje',
                                                          'required': 'True',
                                                          'autocomplete': 'off'}))
    ladders = forms.CharField(required=False, label='Escaleras',
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Escaleras',
                                                            'autocomplete': 'off'}))
    observation = forms.CharField(required=False,
                                  max_length=450,
                                  widget=forms.Textarea(attrs={'class': 'form-control',
                                                               'rows': '3'}))

    def clean_car(self):
        car = self.cleaned_data['car']
        integra = self.cleaned_data['integra']
        try:
            if integra:
                car = 'I-' + str(car)
            car = Car.objects.get(internal_number=car)
            return car
        except Car.DoesNotExist:
            raise forms.ValidationError('El interno del vehiculo NO EXISTE!!')

    def clean_employee(self):
        employee = self.cleaned_data['employee']
        try:
            employee = Employee.objects.get(item=employee)
            return employee
        except Employee.DoesNotExist:
            raise forms.ValidationError('El item ingresado NO EXISTE')

    def clean_observation(self):
        observation = self.cleaned_data['observation']
        if observation:
            return observation
        else:
            return ''

class SelectWorkshopForm(forms.Form):
    workshop = forms.ModelChoiceField(queryset=Workshop.objects.filter(is_active=True),
                                      widget=forms.Select(attrs={'class': 'form-control'}),
                                      initial=0)

