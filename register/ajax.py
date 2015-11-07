
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.http import Http404

from maintenance.models import MaintenanceWorkshop
from branchoffice.models import Car, GuardsToBranchoffice
from staff.models import Guard
from register.models import StatusCar

import json
import datetime

@login_required
@csrf_protect
def validation_car(request):
    c = {}
    c.update(csrf(request))
    if request.is_ajax():
        item_car = request.GET.get('car', '')
        try:
            car = Car.objects.get(internal_number=item_car)
        except Car.DoesNotExist:
            raise Http404
        try:
            status = StatusCar.objects.get(car=car)
        except StatusCar.DoesNotExist:
            raise Http404
        response_data = {}
        if status.last_register_car is not None:
            last_register_car = status.last_register_car
            response_data['in_moving'] = status.in_moving
            response_data['driver'] = last_register_car.employee.item
            response_data['km'] = last_register_car.register_km
            response_data['ladders'] = last_register_car.ladders
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        html = '<p>Funcion no aceptada</p>'
        return HttpResponse(html)

@login_required
@csrf_protect
def validation_car_sidebar(request):
    c = {}
    c.update(csrf(request))
    if request.is_ajax():
        item_car = request.POST.get('car', '')
        try:
            car = Car.objects.get(internal_number=item_car)
        except Car.DoesNotExist:
            raise Http404
        ######### ESTA SECCION SOLO PERMITE A LOS GUARDIAS REGISTRAR ######
        try:
            guard = Guard.objects.get(staff=request.user.staff)
            branchoffice = GuardsToBranchoffice.objects.filter(guard=guard).filter(is_active=True)
            parking = branchoffice[0].branchoffice
        except Guard.DoesNotExist:
            return HttpResponse('<div class="alert fade in alert-danger">' +
                                '    <b>ERROR:</b> No tiene permisos para guardar registros' +
                                '</div>')
        if car.branchoffice != parking:
            return HttpResponse('<div class="alert fade in alert-warning">' +
                                '    <b>ALERTA:</b> Este vehiculo no pertenece ' +
                                '    al parqueo <b>' + parking.name + '</b> use ' +
                                '    la opcion <b>"Vehiculos Externos"</b> en Opciones.' +
                                '</div>')


        ############### FIN DE LA SECCION ################################

        try:
            status = StatusCar.objects.get(car=car)
        except StatusCar.DoesNotExist:
            raise Http404
        if status.last_register_car is not None:
            last_register = status.last_register_car
            car = last_register.car
            if car.is_active:
                in_workshop = False
            else:
                m = MaintenanceWorkshop.objects.filter(car=car).filter(fixed=False)
                if len(m) > 0:
                    in_workshop = True
                else:
                    in_workshop = False

            if last_register.employee.is_motorist:
                if last_register.employee.get_motorist().expiration_date:
                    alert_license = last_register.employee.get_motorist().expiration_date < datetime.date.today()
                else:
                    alert_license = True
            else:
                alert_license = False
            response = TemplateResponse(request,
                                        'last_register.html',
                                        {'register': last_register,
                                        'employee': last_register.employee,
                                        'alert_license': alert_license,
                                        'car': car,
                                        'in_moving': status.in_moving,
                                        'in_workshop': in_workshop,
                                        'parking': status.parking,
                                        'edit_register_url': last_register.get_absolute_url})
            return response
        else:
            return HttpResponse('<h4>No se encontro ningun registro</h4>' +
                                '<div class="alert fade in alert-warning">' +
                                '    Tenga en cuenta de lo que va ha registrar ' +
                                '    sera guardado como <b>SALIDA</b> del vehiculo' +
                                '</div>')

@login_required
def delete_date_session(request):
    if request.is_ajax():
        if 'stick_date' in request.session:
            del request.session['stick_date']
            print 'se borro la fecha de la session'
    return HttpResponse('<p>se elimino la fecha</p>')
