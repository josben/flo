from django.db import models
from staff.models import Guard

from staff.models import Employee

class BranchOffice(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=450, blank=True, null=True)
    address = models.CharField(max_length=350, blank=True, null=True)
    guards = models.ManyToManyField(Guard, through='GuardsToBranchoffice')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/branchoffice/%i' % self.id

class GuardsToBranchoffice(models.Model):
    branchoffice = models.ForeignKey(BranchOffice)
    guard = models.ForeignKey(Guard)
    date_joined = models.DateField(auto_now_add=True)
    date_end = models.DateField(blank=True, null=True)
    observation = models.CharField(max_length=450)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.guard) + ' (' + self.branchoffice.name + ')'

    def get_absolute_url(self):
        return '/branchoffice/guardstobranchoffice/%i' % self.id

    def get_date_joined_str(self):
        return self.date_joined.strftime("%d/%m/%y")

class WorkUnit(models.Model):
    branchoffice = models.ForeignKey(BranchOffice, blank=True, null=True)
    name = models.CharField(max_length=45, unique=True)
    description = models.CharField(max_length=450, blank=True, null=True)

    def __unicode__(self):
        return self.name

class TmpWorkUnit(models.Model):
    branchoffice = models.ForeignKey(BranchOffice, blank=True, null=True)
    name = models.CharField(max_length=45, unique=True)
    description = models.CharField(max_length=450,blank=True, null=True)

class EmployeeWorkUnit(models.Model):
    employee = models.ForeignKey(Employee)
    workunit = models.ForeignKey(WorkUnit)
    position = models.CharField(max_length=45, blank=True, null=True)
    date_joined = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.workunit.name

class TmpEmployeeWorkUnit(models.Model):
    employee = models.ForeignKey(Employee)
    workunit = models.ForeignKey(TmpWorkUnit)
    position = models.CharField(max_length=45, blank=True, null=True)
    date_joined = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class TypeMotorized(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=300, blank=True, null=True)

    def __unicode__(self):
        return self.name

class Car(models.Model):
    branchoffice = models.ForeignKey(BranchOffice, blank=True, null=True)
    date_joined = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    type_motorized = models.ForeignKey(TypeMotorized, blank=True, null=True)

    #los vehiculos alquilados no tienen numero interno
    internal_number = models.CharField(max_length=20,
                                       unique=True,
                                       blank=True, null=True)

    traction = models.CharField(max_length=30, blank=True, null=True)
    license_plate = models.CharField(max_length=20, unique=True)
    model_year = models.CharField(max_length=15, blank=True, null=True)
    manufacturer = models.CharField(max_length=30, blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True)
    cylinder_capacity = models.CharField(max_length=30, blank=True, null=True)
    chassis = models.CharField(max_length=30, blank=True, null=True)
    number_engine = models.CharField(max_length=30, blank=True, null=True)
    current_km = models.IntegerField(blank=True, null=True)
    revert_km = models.BooleanField(default=False)
    observation = models.CharField(max_length=450, blank=True, null=True)
    rental_car = models.BooleanField(default=False)
    external_car = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __unicode__(self):
        if self.rental_car or self.external_car:
            return self.license_plate
        else:
            return self.internal_number

    def get_absolute_url(self):
        return '/branchoffice/car/%i' % self.id

    def get_current_km(self):
        if self.current_km is None:
            return '---'
        else:
            return self.current_km

class Ladder(models.Model):
    code = models.CharField(max_length=15, unique=True)
    date_created = models.DateField(auto_now_add=True)
    observation = models.CharField(max_length=450, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.code

# InParking: Esta clase nos permite ver que autos estan en parqueo y estan
# listos para salir.
# in_parking: si es true quiere decir que esta en parqueo listo para salir
# output: si esta False hasta el final del dia quiere decir que no salio en
# todo el dia.
# Para iniciar el siguiente dia todos los autos se ponen en True en in_parking y
# en False en output.
# Pero antes de actualizar esos datos se registran todos los autos que estan con
# False en output en la tabla de register.CarsWithNoExits que es donde se
# registran los autos que no salieron.
class InParking(models.Model):
    car = models.ForeignKey(Car)
    branchoffice = models.ForeignKey(BranchOffice)
    in_parking = models.BooleanField(default=True)
    output = models.BooleanField(default=False)

