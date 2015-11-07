from django.db import models

from staff.models import Employee
from guest.models import Guest
from branchoffice.models import Car, BranchOffice, Ladder
from core.models import User

from django.utils.translation import gettext_lazy as _

class CarRegistration(models.Model):
    EVENT_CHOICES = (
            ('entrada', _('input')),
            ('salida', _('output')),
    )

    employee = models.ForeignKey(Employee, blank=True, null=True)
    guest = models.ForeignKey(Guest, blank=True, null=True)
    car = models.ForeignKey(Car)
    branch_office = models.ForeignKey(BranchOffice)
    register_date = models.DateField()
    register_time = models.DateTimeField()
    register_km = models.IntegerField()
    ladders = models.CharField(max_length=50, blank=True, null=True)
    date_modification = models.DateTimeField()
    event = models.CharField(max_length=10, choices=EVENT_CHOICES)
    owner = models.ForeignKey(User)
    observation = models.CharField(max_length=450, blank=True, null=True)

    class Meta:
        permissions = (
            ('view_register', 'Puede ver el detalle de registro'),
        )

    def __unicode__(self):
        return 'id_reg: ' + str(self.id) + ' car: ' + str(self.car)

    def get_absolute_url(self):
        return '/register/%i' % self.id

    def get_date_str(self):
        return self.register_date.strftime("%d/%m/%y")

class AllCarRegistration(models.Model):
    car = models.ForeignKey(Car)
    custody_out = models.ForeignKey(Employee, related_name='custody_out',
                                    blank=True, null=True)
    custody_in = models.ForeignKey(Employee, related_name='custody_in',
                                   blank=True, null=True)
    other_driver = models.ForeignKey(Guest, blank=True, null=True)
    parking_out = models.ForeignKey(BranchOffice, related_name='parking_out',
                                    blank=True, null=True)
    parking_in = models.ForeignKey(BranchOffice, related_name='parking_in',
                                   blank=True, null=True)
    # register_date: este es la fecha que a sido creado el registro
    register_date = models.DateField()
    time_out = models.DateTimeField(blank=True, null=True)
    km_out = models.IntegerField(blank=True, null=True)
    time_in = models.DateTimeField(blank=True, null=True)
    km_in = models.IntegerField(blank=True, null=True)
    ladders_out = models.CharField(max_length=50, blank=True, null=True)
    ladders_in = models.CharField(max_length=50, blank=True, null=True)
    register_out = models.ForeignKey(CarRegistration,
                                     blank=True, null=True,
                                     related_name='register_out')
    register_in = models.ForeignKey(CarRegistration,
                                    blank=True, null=True,
                                    related_name='register_in')
    # Si el vehiculo no sale is_complete es True
    is_complete = models.BooleanField()

    # True: si el vehiculo no salio de parqueo
    # False: si el vehiculo salio de parqueo
    #in_parking = models.BooleanField(default=False)
    observation = models.CharField(max_length=450, blank=True, null=True)

    #alert: este campo es para senialar que el registro tiene una alerta, puede ser
    # que le ocurrio algun robo, choque, escaleras incompletas. El administrado
    # es el unico que puede quitar esta alerta.
    # Este alert es diferente de is_complete, is_complete solo verifica que el
    # registro tenga hora de salida y llegada.
    # THINKING: se probara usando las notificaciones, antes de habilitar esta
    # opcion.
    #alert = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.car)

    def diferent_custody(self):
        if self.custody_out != self.custody_in:
            return True
        else:
            return False

    def get_diff_km(self):
        if self.km_in is None or self.km_out is None:
            return '---'
        else:
            return self.km_in - self.km_out

    def get_absolute_url(self):
        return '/register/%i' % self.id

    def get_date_str(self):
        return self.register_date.strftime("%d/%m/%y")

    def get_time_in_str(self):
        if self.time_in is None:
            return '---'
        else:
            return self.time_in.strftime("%H:%M")

    # TODO: Este metodo hay que mejorar, para que haga una mejor comparacion y
    # saber que escalera falta, seria bueno usar expresiones regulares como esta:
    # re.findall(r"[\w]+", cadena), esto devuelve una lista.
    def compareLadders(self):
        if self.ladders_out != self.ladders_in:
            return True
        else:
            return False

class LadderRegistration(models.Model):
    car_register = models.ForeignKey(CarRegistration)
    ladders = models.ForeignKey(Ladder)

class ObservationsRegCar(models.Model):
    car_register = models.ForeignKey(CarRegistration)
    description = models.CharField(max_length=450, blank=True, null=True)
    date_created = models.DateField()

class StatusCar(models.Model):
    car = models.ForeignKey(Car, unique=True)
    last_register_car = models.ForeignKey(CarRegistration,
                                          blank=True, null=True)
    # es True si el estado de last_register_car es 'output' o salida
    in_moving = models.BooleanField(default=False)
    parking = models.ForeignKey(BranchOffice)

    def __unicode__(self):
        return self.car.__unicode__()

    def get_status(self):
        return self.in_moving

    def get_parking(self):
        if self.last_register_car is not None:
            return self.last_register_car.branchoffice
        else:
            return None

    def updateStatus(self, register):
        if self.in_moving:
            self.car.current_km = register.register_km
            self.car.save()
            reg_complete = AllCarRegistration(car=self.last_register_car.car,
                                              custody_out=self.last_register_car.employee,
                                              custody_in=register.employee,
                                              parking_out=self.last_register_car.branch_office,
                                              parking_in=register.branch_office,
                                              register_date=self.last_register_car.register_date,
                                              time_out=self.last_register_car.register_time,
                                              km_out=self.last_register_car.register_km,
                                              ladders_out=self.last_register_car.ladders,
                                              time_in=register.register_time,
                                              km_in=register.register_km,
                                              ladders_in=register.ladders,
                                              register_out=self.last_register_car,
                                              register_in=register,
                                              is_complete=True)
            reg_complete.save()
            self.in_moving = False
            self.last_register_car = register
            self.parking = register.branch_office
            self.save()
        else:
            self.in_moving = True
            self.last_register_car = register
            self.save()

            if self.car.current_km is None:
                self.car.current_km = register.register_km
                self.car.save()

# GuestRegistration: Registra el ingreso de personas a oficinas
class GuestRegistration(models.Model):
    guest = models.ForeignKey(Guest)
    register_date = models.DateField(auto_now_add=True)
    time_entry = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(blank=True, null=True)
    reason = models.CharField(max_length=450)
    branchoffice = models.ForeignKey(BranchOffice)
    owner = models.ForeignKey(User)

    def get_date_str(self):
        return self.register_date.strftime("%d/%m/%y")

    def get_time_out_str(self):
        if self.time_out is None:
            return '---'
        else:
            return self.time_out.strftime("%H:%M")

# CarsWithNoExits: En esta tabla se registran todos los autos que no tuvieron
# ninguna salida en el dia
class CarsWithNoExits(models.Model):
    car = models.ForeignKey(Car)
    parking = models.ForeignKey(BranchOffice)
    register_date = models.DateField()
    observation = models.CharField(max_length=450)

# CarsCurrentState: nos permite saber cual fue la ultima salida del vehiculo
# y en donde termino
class CarsCurrentState(models.Model):
    car = models.ForeignKey(Car)
    last_parking = models.ForeignKey(BranchOffice)
    last_register = models.ForeignKey(CarRegistration, blank=True, null=True)
    date = models.DateTimeField()
    observation = models.CharField(max_length=450)

# En esta tabla se pretende guardar la fecha de los registros que se estan
# guardando por el guardia de un parqueo.
class LastDateRegisterByBranchoffice(models.Model):
    branchoffice = models.ForeignKey(BranchOffice, unique=True)
    last_date_registers = models.DateField()

# Para los registros temporales, si llega a tener un par, de salida y entrada se
# carga a la tabla AllCarRegistration.
class ForeignCarRegistrationIO(models.Model):
    TYPE_EVENT = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida')
    )

    car = models.ForeignKey(Car)
    parking = models.ForeignKey(BranchOffice)
    register_in = models.ForeignKey(CarRegistration,
                                    related_name='tmp_register_in',
                                    blank=True, null=True)
    register_out = models.ForeignKey(CarRegistration,
                                     related_name='tmp_register_out',
                                     blank=True, null=True)
    # date_modification: es la ultima fecha que ocurrio un evento con este
    # vehiculo.
    date_modification = models.DateTimeField(auto_now_add=True)
    last_event = models.CharField(max_length=15, choices=TYPE_EVENT)

    def __unicode__(self):
        return 'Car: ' + str(self.car) + ' Evento: ' + self.last_event

    def get_last_register(self):
        if self.last_event == 'entrada':
            return self.register_in
        else:
            return self.register_out

    def verifyRegister(self):
        if self.last_event == 'entrada':
            if self.register_out:
                if self.register_out.register_time < self.register_in.register_time:
                    reg_complete = AllCarRegistration(car=self.car,
                                                      custody_out=self.register_out.employee,
                                                      custody_in=self.register_in.employee,
                                                      parking_out=self.parking,
                                                      parking_in=self.parking,
                                                      register_date=self.register_in.register_date,
                                                      time_out=self.register_out.register_time,
                                                      km_out=self.register_out.register_km,
                                                      ladders_out=self.register_out.ladders,
                                                      time_in=self.register_in.register_time,
                                                      km_in=self.register_in.register_km,
                                                      ladders_in=self.register_in.ladders,
                                                      register_out=self.register_out,
                                                      register_in=self.register_in,
                                                      is_complete=True)
                    reg_complete.save()

