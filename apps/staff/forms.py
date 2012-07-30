
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from flo.apps.staff.models import Staff, Unit, Role, Driver
from django.contrib.admin import widgets
"""
SALUDATION_CHOICES = (
    ('1', 'Dr'),
    ('2', 'Sr.'),
    ('3', 'Srta.'),
    ('4', 'Sra.'),
)

TYPE_DOCUMENT_CHOICES = (
    ('CI', 'Carne de Identidad'),
    ('NI', 'Numero interno'),
)

JOB_TITLE_CHOICES = (
    ('1', 'Licenciado'),
    ('2', 'Ingenierio'),
    ('3', 'Tecnico'),
    ('4', 'Sr./Sra.'),
    ('5', 'Estudiante'),
)

JOB_ROLE_CHOICES = (
    ('1', 'Gerente'),
    ('2', 'Secretaria'),
    ('3', 'Conductor de vehiculo'),
)

LOCALE_CHOICES = (
    ('LP', 'La Paz'),
    ('SC', 'Santa Cruz'),
    ('PD', 'Pando'),
    ('BN', 'Beni'),
    ('OR', 'Oruro'),
    ('PT', 'Potosi'),
    ('TJ', 'Tarija'),
    ('CH', 'Chuquisaca'),
    ('CB', 'Cochabamba'),
)
class StaffForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True, error_messages={'required': 'Ingrese un nombre por favor'})
    last_name = forms.CharField(max_length=50, required=True, error_messages={'required': 'Ingrese un nombre por favor'})
    type_doc = forms.ChoiceField(choices=TYPE_DOCUMENT_CHOICES)
    value_doc = forms.CharField(max_length=15, required=True, error_messages={'required': 'Ingrese un valor valido'})
    locale_issue = forms.ChoiceField(choices=LOCALE_CHOICES, required=True, error_messages={'required': 'Elija una opcion'})
    job_title = forms.ChoiceField(choices=JOB_TITLE_CHOICES, required=True, error_messages={'required': 'Elija una opcion'})
    job_role = forms.ChoiceField(choices=JOB_ROLE_CHOICES, required=True, error_messages={'required': 'Elija una opcion'})
    #TODO: unit, role
    avatar = forms.ImageField(required=True, error_messages={'required': 'Suba una imagen'})
"""

class StaffForm(forms.ModelForm):
#    unit = forms.ModelChoiceField(queryset=Unit.objects.all())
#    role = forms.ModelChoiceField(queryset=Role.objects.all())
    class Meta:
        model = Staff
 #       exclude = ('unit', 'role')

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role

class DriverForm(forms.ModelForm):
    date_issue = forms.DateField(required = True, widget = forms.DateInput(format='%dd/%mm/%yy'),
            help_text=_('Formato: MM/DD/YY')) #, input_formats='%dd/%mm/%yy')
    date_expiration = forms.DateField(required = True, widget = forms.DateInput(format='%dd/%mm/%yy'),
            help_text=_('Formato: MM/DD/YY')) #, input_formats='%dd/%mm/%yy')
    class Meta:
        model = Driver
        exclude = ('staff')

