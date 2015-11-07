
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.utils.html import escape #strip_tags, quita los tags html

from notifications.models import Notifications
from staff.models import Guard
from branchoffice.models import GuardsToBranchoffice

from datetime import datetime

@login_required
def viewNotification(request, notification_id):
    c = {}
    c.update(csrf(request))
    if request.is_ajax():
        ns = Notifications.objects.get(id=notification_id)
        ns.date_closed = datetime.today()
        ns.is_closed = True
        ns.save()
        if ns.sender.staff:
            if ns.sender.staff.is_guard:
                guard = Guard.objects.get(staff=ns.sender.staff)
                gbo = GuardsToBranchoffice.objects.get(guard=guard)
                parking = gbo.branchoffice.name
            else:
                parking = ''
        else:
            parking = ''
        if ns.notification.type_notification == '1':
            tn = 'De un empleado'
        elif ns.notification.type_notification == '2':
            tn = 'De un vehiculo'
        elif ns.notification.type_notification == '3':
            tn = 'De una persona'
        elif ns.notification.type_notification == '4':
            tn = 'De un registro'
        elif ns.notification.type_notification == '5':
            tn = 'De una escalera'
        else:
            tn = 'Otros'
        if ns.priority == 1:
            alert = 'danger'
        elif ns.priority == 2:
            alert = 'warning'
        else:
            alert = 'info'
        return HttpResponse('<div class="alert fade in alert-'+ alert +'">' +
                            '    <b>Tipo de notificacion: </b>' + tn + '</br>' +
                            '    <b>Resumen: </b>' + escape(ns.notification.abstract) + '</br>' +
                            '    <b>Detalle: </b>' + escape(ns.notification.description) + '</br>' +
                            '    <b>Fecha: </b>' + ns.notification.date_created.strftime('%d/%m/%Y') + '</br>' +
                            '    <b>Envia: </b>' + str(ns.sender) + '</br>' +
                            '    <b>Oficina: </b>' + parking +
                            '</div>')
    else:
        return HttpResponse('<b>Ocurrio un error</b>')

