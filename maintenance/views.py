
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import RequestContext

from maintenance.models import (MaintenanceWorkshop,
                                MaintenanceProgram,
                                Workshop)
from maintenance.forms import FormMaintenanceProgram, FormWorkshop
from branchoffice.models import Car

import datetime

@login_required
def index(request):
    m_all = MaintenanceWorkshop.objects.all().order_by('-date_joined')
    return render(request,
                  'maintenance.html',
                  {'m_list': m_all})

@login_required
def inWorkshop(request):
    m_all = MaintenanceWorkshop.objects.filter(fixed=False)
    return render(request,
                  'maintenance.html',
                  {'m_list': m_all})

@login_required
def viewCarInWorkshop(request, maintenance_id):
    m_car = MaintenanceWorkshop.objects.get(id=maintenance_id)
    return render(request,
                  'view_car_workshop.html',
                  {'workshop': m_car})

@login_required
def fixedCar(request, maintenance_id):
    m_car = MaintenanceWorkshop.objects.get(id=maintenance_id)
    m_car.date_out = datetime.date.today()
    m_car.fixed = True
    m_car.save()
    m_car.car.is_active = True
    m_car.car.save()
    return HttpResponseRedirect('/maintenance/')

@login_required
def maintenanceProgramClose(request, mp_id):
    mp = MaintenanceProgram.objects.get(id=mp_id)
    if not mp.is_closed:
        mp.is_closed = True
        mp.date_closed = datetime.date.today()
        mp.save()
        messages.add_message(request,
                             messages.SUCCESS,
                             'Se cancelo el mantenimiento para: ' + mp.car.internal_number)
    else:
        if mp.next_date_maintenance > datetime.date.today():
            mp.is_closed = False
            mp.date_closed = None
            mp.save()
            messages.add_message(request,
                                messages.SUCCESS,
                                'Se habilito el mantenimiento para: ' + mp.car.internal_number)

    return HttpResponseRedirect('/maintenance/program/')

@login_required
def searchWorkshopByCar(request):
    if request.method == 'GET':
        try:
            internal_number = request.GET['car']
            car = Car.objects.get(internal_number=internal_number)
            ws = MaintenanceWorkshop.objects.filter(car=car).order_by('-date_joined')
            if not ws:
                messages.add_message(request,
                                     messages.WARNING,
                                     'No se encontro ningun ingreso.')
            return render(request,
                        'maintenance.html',
                        {'m_list': ws})
        except Car.DoesNotExist:
            messages.add_message(request,
                                 messages.ERROR,
                                 'El interno de vehiculo no existe.')
            return HttpResponseRedirect('/maintenance/')

@login_required
def searchMaintenanceProgramByCar(request):
    if request.method == 'GET':
        try:
            internal_number = request.GET['car']
            car = Car.objects.get(internal_number=internal_number)
            mp = MaintenanceProgram.objects.filter(car=car).order_by('-next_date_maintenance')
            if not mp:
                messages.add_message(request,
                                     messages.WARNING,
                                     'No se encontro ningun ingreso.')
            return render(request,
                        'maintenance_program.html',
                        {'mp_list': mp})
        except Car.DoesNotExist:
            messages.add_message(request,
                                 messages.ERROR,
                                 'El interno de vehiculo no existe.')
            return HttpResponseRedirect('/maintenance/program/')

@login_required
def maintenanceProgram(request):
    mp = MaintenanceProgram.objects.all()
    return render(request,
                  'maintenance_program.html',
                  {'mp_list': mp})

@login_required
def maintenanceProgramCar(request):
    if request.method == 'POST':
        form = FormMaintenanceProgram(request.POST)
        if form.is_valid():
            workshop = form.cleaned_data['workshop']
            internal_number = form.cleaned_data['internal_number']
            next_km_maintenance = form.cleaned_data['next_km_maintenance']
            next_date_maintenance = form.cleaned_data['next_date_maintenance']
            reason = form.cleaned_data['reason']

            car = Car.objects.get(internal_number=internal_number)
            lm = MaintenanceWorkshop.objects.filter(car=car).filter(fixed=True).order_by('-date_out')
            if lm:
                lm = lm[0]
                pm = MaintenanceProgram(car=car,
                                        workshop=workshop,
                                        last_maintenance=lm,
                                        last_km_maintenance=lm.register.register_km,
                                        last_date_maintenance=lm.date_out,
                                        next_km_maintenance=next_km_maintenance,
                                        next_date_maintenance=next_date_maintenance,
                                        reason=reason,
                                        date_asigned=datetime.date.today())
                pm.save()

            else:
                pm = MaintenanceProgram(car=car,
                                        workshop=workshop,
                                        next_km_maintenance=next_km_maintenance,
                                        next_date_maintenance=next_date_maintenance,
                                        reason=reason,
                                        date_asigned=datetime.date.today())
                pm.save()

            messages.add_message(request,
                                messages.SUCCESS,
                                'Se guardo satisfactoriamente para el vehiculo %s ' % car)
            return HttpResponseRedirect('/maintenance/program/')
        else:
            messages.add_message(request,
                                messages.ERROR,
                                'Los datos ingresados son incorrectos.')
            return render_to_response('form_program_maintenance.html', {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = FormMaintenanceProgram()
        return render_to_response('form_program_maintenance.html', {'form': form},
                                    context_instance=RequestContext(request))

@login_required
def newWorkshop(request):
    if request.method == 'POST':
        form = FormWorkshop(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/maintenance/')
        else:
            messages.add_message(request,
                                messages.ERROR,
                                'Los datos ingresados son incorrectos.')
            return render_to_response('form_workshop.html', {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = FormWorkshop()
        return render_to_response('form_workshop.html', {'form': form},
                                  context_instance=RequestContext(request))

@login_required
def workshopList(request):
    wl = Workshop.objects.all()
    return render(request,
                  'workshop.html',
                  {'w_list': wl})

@login_required
def carsInWorkshop(request, workshop_id):
    workshop = Workshop.objects.get(id=workshop_id)
    mw = MaintenanceWorkshop.objects.filter(workshop=workshop)
    return render(request,
                  'maintenance.html',
                  {'m_list': mw})

@login_required
def onOffWorkshop(request, workshop_id):
    workshop = Workshop.objects.get(id=workshop_id)
    if workshop.is_active:
        workshop.is_active = False
        workshop.save()
    else:
        workshop.is_active = True
        workshop.save()
    return HttpResponseRedirect('/maintenance/workshop/list/')

