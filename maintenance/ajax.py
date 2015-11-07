
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.core.context_processors import csrf

from branchoffice.models import Car
from maintenance.models import MaintenanceWorkshop

def lastMaintenance(request):
    c = {}
    c.update(csrf(request))
    if request.is_ajax():
        internal_number = request.POST.get('internal_number', '')
        try:
            car = Car.objects.get(internal_number=internal_number)
            if not car.is_active:
                mw = MaintenanceWorkshop.objects.filter(car=car).filter(fixed=False)
                if mw:
                    return HttpResponse('<div class="alert fade in alert-warning">' +
                                        '    <b>ALERTA:</b> Este vehiculo esta ' +
                                        '    actualmente en taller.' +
                                        '    <a href="' + mw[0].get_absolute_url() + '/view/" class="btn btn-primary">' +
                                        '       Ver detalle' +
                                        '    </a>' +
                                        '</div>')
                else:
                    return HttpResponse('<div class="alert fade in alert-warning">' +
                                        '    <b>ALERTA:</b> Este vehiculo esta como ' +
                                        '    inactivo, vea el listado de vehiculos y ' +
                                        '    activelo como administrador.' +
                                        '    <a href="/branchoffice/list/cars/" class="btn btn-primary">' +
                                        '       Ver lista de vehiculos' +
                                        '    </a>' +
                                        '</div>')
            else:
                mw = MaintenanceWorkshop.objects.filter(car=car).filter(fixed=True).order_by('-date_out')
                if mw:
                    response = TemplateResponse(request,
                                                'last_maintenance.html',
                                                {'last_maintenance': mw[0],
                                                 'car': car})
                    return response
                else:
                    return HttpResponse('<div class="alert fade in alert-info">' +
                                        '    <b>INFORMACION:</b> Este vehiculo no tiene ' +
                                        '    ningun registro de un mantenimiento ' +
                                        '    anterior.</br>' +
                                        '    <b>Kilometraje actual: </b>' + str(car.current_km)  +
                                        '</div>')
        except Car.DoesNotExist:
            return HttpResponse('<div class="alert fade in alert-danger">' +
                                '    <b>ERROR:</b> Este vehiculo no existe.' +
                                '</div>')


