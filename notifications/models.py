from django.db import models
from core.models import User
from django.utils.translation import gettext_lazy as _

from register.models import CarRegistration, GuestRegistration
from branchoffice.models import Car
from staff.models import Employee

class Notification(models.Model):
    TYPE_NOTIFICATION_CHOICES = (
        ('1', 'De un empleado'),
        ('2', 'De un vehiculo'),
        ('3', 'De una persona'),
        ('4', 'De un registro'),
        ('5', 'De una escalera'),
        ('6', 'Otros'),
    )

    type_notification = models.CharField(max_length=1,
                                         choices=TYPE_NOTIFICATION_CHOICES)
    abstract = models.CharField(max_length=130)
    description = models.CharField(max_length=450, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ('view_notification', 'Puede ver la notificacion'),
        )

    def __unicode__(self):
        return self.abstract

    def get_type_notification(self):
        if self.type_notification == '1':
            return 'Empleado'
        elif self.type_notification == '2':
            return 'Vehiculo'
        elif self.type_notification == '3':
            return 'Persona'
        elif self.type_notification == '4':
            return 'Registro'
        elif self.type_notification == '5':
            return 'Escalera'
        else:
            return 'Otros'

class NotificationsRegisterCar(models.Model):
    notification = models.ForeignKey(Notification)
    register_car = models.ForeignKey(CarRegistration)

class NotificationsRegisterGuest(models.Model):
    notification = models.ForeignKey(Notification)
    register_guest = models.ForeignKey(GuestRegistration)

class NotificationsEmployee(models.Model):
    notification = models.ForeignKey(Notification)
    employee = models.ForeignKey(Employee)

class NotificationsCar(models.Model):
    notification = models.ForeignKey(Notification)
    car = models.ForeignKey(Car)

class Notifications(models.Model):
    PRIORITY_CHOICES = (
        (1, 'Prioridad Alta'),
        (2, 'Prioridad Media'),
        (3, 'Prioridad Baja'),
    )

    owner = models.ForeignKey(User, related_name='owner')
    sender = models.ForeignKey(User, related_name='sender')
    notification = models.ForeignKey(Notification)
    date_closed = models.DateTimeField(blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    is_closed = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('view_notifications', 'Puede ver las notificaciones'),
        )

    def get_priority(self):
        if self.priority == 1:
            return 'Alta'
        elif self.priority == 2:
            return 'Media'
        else:
            return 'Baja'

