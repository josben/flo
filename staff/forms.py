
from django import forms

from .models import Staff, Employee
from company.models import Company
from branchoffice.models import BranchOffice, WorkUnit

from bootstrap3_datetime.widgets import DateTimePicker

import datetime

class StaffForm(forms.ModelForm):
    TYPE_STAFF = (
        ('employee', 'Personal'),
        ('guard', 'Guardia')
    )
    type_staff = forms.ChoiceField(choices=TYPE_STAFF,
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Staff
        exclude = ['date_joined', 'date_end', 'is_active']
        widgets = {
                'birth_date': DateTimePicker(options={"format":"DD/MM/YYYY", "pickTime": False}),
                'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Nombre'}),
                'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Apellido'}),
                'val_document': forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': 'Numero de documento'}),
                'number_phone': forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': 'Numero de telefono'}),
                'locale_issue': forms.Select(attrs={'class': 'form-control'}),
                'locale_issue_other': forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Nacionalidad'}),
                'type_document': forms.Select(attrs={'class': 'form-control'}),
                'gender': forms.Select(attrs={'class': 'form-control'}),
                'photo' : forms.FileInput(),
                'about': forms.Textarea(attrs={'rows': '3',
                                               'class': 'form-control',
                                               'placeholder': 'Ingrese alguna descripcion'})
        }

    def clean_val_document(self):
        ci = self.cleaned_data['val_document']
        try:
            doc = Staff.objects.get(val_document=ci)
            raise forms.ValidationError('Este CI ya existe, es de: ' + str(doc))
        except Staff.DoesNotExist:
            return ci

class StaffEditForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ['date_end', 'is_active', 'is_employee', 'is_guard']
        widgets = {
                'birth_date': DateTimePicker(options={"format":"DD/MM/YYYY", "pickTime": False}),
                'date_joined': DateTimePicker(options={"format":"DD/MM/YYYY", "pickTime": False}),
                'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Nombre'}),
                'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Apellido'}),
                'val_document': forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': 'Numero de documento'}),
                'number_phone': forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': 'Numero de telefono'}),
                'locale_issue': forms.Select(attrs={'class': 'form-control'}),
                'locale_issue_other': forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Nacionalidad'}),
                'type_document': forms.Select(attrs={'class': 'form-control'}),
                'gender': forms.Select(attrs={'class': 'form-control'}),
                'photo' : forms.FileInput(),
                'about': forms.Textarea(attrs={'rows': '3',
                                               'class': 'form-control',
                                               'placeholder': 'Ingrese alguna descripcion'})
        }

class EmployeeForm(forms.Form):
    CATEGORY_CHOICES = (
        ('', ''),
        ('P', 'P - Particular'),
        ('A', 'A - Novato'),
        ('B', 'B - Intermedio'),
        ('C', 'C - Experto'),
        ('M', 'M - Moto'),
        )
    item = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Item'}))
    corporate_number = forms.IntegerField(required=False,
                                          widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': 'Corporativo'}))
    workunit = forms.ModelChoiceField(queryset=WorkUnit.objects.all().order_by('name'),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    position = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Cargo'}))
    is_motorist = forms.BooleanField(required=False)
    driver_category = forms.ChoiceField(choices=CATEGORY_CHOICES,
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        required=False)
    expiration_date = forms.DateField(widget=DateTimePicker(options={"format":"DD/MM/YYYY", "pickTime": False}),
                                      required=False)

    def clean_item(self):
        item = self.cleaned_data['item']
        try:
            e = Employee.objects.get(item=item)
            raise forms.ValidationError('El item ya existe y esta asignado a: ' + str(e.staff))
        except Employee.DoesNotExist:
            return item

class GuardForm(forms.Form):
    company = forms.ModelChoiceField(queryset=Company.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    branchoffice = forms.ModelChoiceField(queryset=BranchOffice.objects.all(),
                                          widget=forms.Select(attrs={'class': 'form-control'}))
    observation = forms.CharField(required=False,
                                  widget=forms.Textarea(attrs={'class': 'form-control',
                                                               'row': '3',
                                                               'placeholder': 'Ingrese alguna descripcion'}))

    def clean_observation(self):
        observation = self.cleaned_data['observation']
        if observation:
            return observation
        else:
            return ''

class UserForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Correo electronico'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password'}))
    is_admin = forms.BooleanField(required=False)

class MotoristUpdateForm(forms.Form):
    CATEGORY_CHOICES = (
        ('', ''),
        ('P', 'P - Particular'),
        ('A', 'A - Novato'),
        ('B', 'B - Intermedio'),
        ('C', 'C - Experto'),
        ('M', 'M - Moto'),
        )

    driver_category = forms.ChoiceField(choices=CATEGORY_CHOICES,
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        required=False)
    expiration_date = forms.DateField(widget=DateTimePicker(options={"format":"DD/MM/YYYY", "pickTime": False}),
                                      required=False)

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data['expiration_date']
        if expiration_date <= datetime.date.today():
            raise forms.ValidationError('La fecha es incorrecta')
        else:
            return expiration_date
