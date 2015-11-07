from django.db import models

from branchoffice.models import Car
from register.models import CarRegistration
from branchoffice.models import BranchOffice

class Workshop(models.Model):
    branchoffice = models.ForeignKey(BranchOffice)
    description = models.CharField(max_length=450)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.branchoffice.name

    def get_absolute_url(self):
        return '/maintenance/workshop/%i' % self.id


class MaintenanceWorkshop(models.Model):
    workshop = models.ForeignKey(Workshop)
    car = models.ForeignKey(Car)
    register = models.ForeignKey(CarRegistration)
    date_joined = models.DateField()
    date_out = models.DateField(blank=True, null=True)
    problem_description = models.CharField(max_length=450)
    fixed = models.BooleanField()
#    service = models.ManyToManyField(MaintenanceProgram, through='ServiceCar')

    def __unicode__(self):
        return str(self.car)

    def get_absolute_url(self):
        return '/maintenance/in/workshop/%i' % self.id

    def get_date_joined_str(self):
        return self.date_joined.strftime("%d/%m/%y")

    def get_date_out_str(self):
        if self.date_out is None:
            return '---'
        else:
            return self.date_out.strftime("%d/%m/%y")

#class ServiceCar(models.Model)

class MaintenanceProgram(models.Model):
    car = models.ForeignKey(Car)
    workshop = models.ForeignKey(Workshop)
    last_maintenance = models.ForeignKey(MaintenanceWorkshop,
                                         blank=True, null=True)
    last_km_maintenance = models.IntegerField(blank=True, null=True)
    last_date_maintenance = models.DateField(blank=True, null=True)
    next_km_maintenance = models.IntegerField(blank=True, null=True)
    next_date_maintenance = models.DateField(blank=True, null=True)
    date_asigned = models.DateField()
    date_closed = models.DateField(blank=True, null=True)
    reason = models.CharField(max_length=450, blank=True, null=True)
    is_closed = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.car)

    def get_absolute_url(self):
        return '/maintenance/program/%i' % self.id


class MaintenanceCar(models.Model):
    car = models.ForeignKey(Car)
    km_interval_maintenance = models.IntegerField()
    km_last_maintenance = models.IntegerField()
    date_last_maintenance = models.DateField()
    next_km_maintenance = models.IntegerField()

