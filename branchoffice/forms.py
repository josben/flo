
from django import forms

from branchoffice.models import BranchOffice, Car, WorkUnit
from bootstrap3_datetime.widgets import DateTimePicker

class BranchOfficeForm(forms.Form):
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
            bo = BranchOffice.objects.get(name=name)
            raise forms.ValidationError('La oficina ya existe: %s' % bo.name)
        except BranchOffice.DoesNotExist:
            return name

class CarToBranchofficeForm(forms.ModelForm):
    TYPE_CAR = (
        ('car_company', 'Auto con item'),
        ('rental_car', 'Auto alquilado')
    )
    type_car = forms.ChoiceField(choices=TYPE_CAR,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Car
        exclude = ['date_end', 'revert_km', 'is_active', 'date_joined']
        widgets = {
                'branchoffice': forms.Select(attrs={'class': 'form-control',
                                                    'autofocus': ''}),
                'type_motorized': forms.Select(attrs={'class': 'form-control'}),
                'internal_number': forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Numero interno'}),
                'traction': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Traccion'}),
                'license_plate': forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Placa de control',
                                                        'required': 'True'}),
                'model_year': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': '2000, 2010, ...'}),
                'manufacturer': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Toyota, Nisan, ...'}),
                'color': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Descripcion del color'}),
                'cylinder_capacity': forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Cilindrada'}),
                'number_engine': forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Numero de motor'}),
                'chassis': forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': 'Chasis'}),
                'current_km': forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': 'Kilometraje actual'}),
                'observation': forms.Textarea(attrs={'rows': '3',
                                                     'class': 'form-control',
                                                     'placeholder': 'Ingrese alguna descripcion'})
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        type_car = self.cleaned_data.get('type_car')
        item = self.cleaned_data.get('internal_number')
        if type_car == 'car_company':
            if not item:
                raise forms.ValidationError('Este auto debe tener un numero' +
                                            ' interno por ser auto de la empresa')
        return cleaned_data

    def clean_internal_number(self):
        item = self.cleaned_data['internal_number']
        try:
            car = Car.objects.get(internal_number=item)
            raise forms.ValidationError('El numero de item ya existe: %s' % car.license_plate )
        except Car.DoesNotExist:
            return item

    def clean_license_plate(self):
        license_plate = self.cleaned_data['license_plate']
        try:
            car = Car.objects.get(license_plate=license_plate)
            raise forms.ValidationError('El auto ya existe con placa: %s' % car.license_plate)
        except Car.DoesNotExist:
            return license_plate

    def clean_chassis(self):
        chassis = self.cleaned_data['chassis']
        if chassis:
            try:
                car = Car.objects.get(chassis=chassis)
                raise forms.ValidationError('El auto ya existe con ese chassis: %s' % car.license_plate)
            except Car.DoesNotExist:
                return chassis
        else:
            return chassis

    def clean_branchoffice(self):
        bo = self.cleaned_data['branchoffice']
        if bo:
            return bo
        else:
            raise forms.ValidationError('Debe destinar a alguna oficina')

class CarDeleteForm(forms.Form):
    observation = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                               'rows': '3',
                                                               'placeholder': 'Porque se elimina',
                                                               'required': ''}))

class CarEditForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ['date_end', 'is_deleted']
        widgets = {
                'branchoffice': forms.Select(attrs={'class': 'form-control',
                                                    'autofocus': ''}),
                'type_motorized': forms.Select(attrs={'class': 'form-control'}),
                'internal_number': forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Numero interno'}),
                'date_joined': DateTimePicker(options={"format":"DD/MM/YYYY", "pickTime": False}),
                'traction': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Traccion'}),
                'license_plate': forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Placa de control',
                                                        'required': 'True'}),
                'model_year': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': '2000, 2010, ...'}),
                'manufacturer': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Toyota, Nisan, ...'}),
                'color': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Descripcion del color'}),
                'cylinder_capacity': forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Cilindrada'}),
                'number_engine': forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Numero de motor'}),
                'chassis': forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': 'Chasis'}),
                'current_km': forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': 'Kilometraje actual'}),
                'observation': forms.Textarea(attrs={'rows': '3',
                                                     'class': 'form-control',
                                                     'placeholder': 'Ingrese alguna descripcion'})
        }

    def clean_branchoffice(self):
        bo = self.cleaned_data['branchoffice']
        if bo:
            return bo
        else:
            raise forms.ValidationError('Debe destinar a alguna oficina')

class WorkUnitForm(forms.Form):
    branchoffice = forms.ModelChoiceField(queryset=BranchOffice.objects.all(),
                                          widget=forms.Select(attrs={'class': 'form-control'}),
                                          required=False)
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': 'Unidad de trabajo'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                               'rows': '3',
                                                               'placeholder': 'Que se hace en la unidad'}),
                                  required=False)

    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            wu = WorkUnit.objects.get(name=name)
            raise forms.ValidationError('La unidad de trabajo ya existe: %s' % wu.name)
        except WorkUnit.DoesNotExist:
            return name
