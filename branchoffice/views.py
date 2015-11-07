
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext
from django.conf import settings
from django.db.utils import IntegrityError
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404

from .models import (BranchOffice,
                     Car, TypeMotorized,
                     Ladder, InParking,
                     GuardsToBranchoffice,
                     WorkUnit)
from .forms import (BranchOfficeForm,
                    CarToBranchofficeForm,
                    CarDeleteForm,
                    CarEditForm,
                    WorkUnitForm)
from register.models import StatusCar
from staff.models import Guard
from maintenance.models import MaintenanceWorkshop

import xlrd, re
import datetime
import pickle

@login_required
def index(request):
    bo_list = BranchOffice.objects.all()

#    paginator = Paginator(branchoffice, 10)
#    page = request.GET.get('page')
#    try:
#        show_lines = paginator.page(page)
#    except PageNotAnInteger:
#        show_lines = paginator.page(1)
#    except EmptyPage:
#        show_lines = paginator.page(paginator.num_pages)

    return render_to_response('branchoffice.html', {'bo_list': bo_list},
            context_instance=RequestContext(request))

@login_required
def newBranchoffice(request):
    if request.method == 'POST':
        form = BranchOfficeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            description = form.cleaned_data['description']

            bo = BranchOffice(name=name,
                              address=address,
                              description=description)
            bo.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'La oficina %s se creo correctamente' % bo.name)
            return HttpResponseRedirect('/branchoffice/')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Los datos que ingreso son incorrectos')
            return render_to_response('branchoffice_form.html', {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = BranchOfficeForm()
        return render_to_response('branchoffice_form.html', {'form': form},
                                  context_instance=RequestContext(request))

@login_required
def newWorkUnit(request):
    if request.method == 'POST':
        form = WorkUnitForm(request.POST)
        if form.is_valid():
            branchoffice = form.cleaned_data['branchoffice']
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']

            wu = WorkUnit(branchoffice=branchoffice,
                          name=name,
                          description=description)
            wu.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'La unidad %s se creo correctamente' % wu.name)
            return HttpResponseRedirect('/staff/only_staff/')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Los datos que ingreso son incorrectos')
            return render_to_response('workunit_form.html', {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = WorkUnitForm()
        return render_to_response('workunit_form.html', {'form': form},
                                  context_instance=RequestContext(request))

@login_required
def newCarToBranchoffice(request):
    if request.method == 'POST':
        form = CarToBranchofficeForm(request.POST)
        if form.is_valid():
            type_car = form.cleaned_data['type_car']
            license_plate = form.cleaned_data['license_plate']
            car = form.save()
            car.date_joined = datetime.date.today()
            car.save()
            if type_car == 'rental_car':
                car.rental_car = True
                car.internal_number = license_plate
                car.save()
            try:
                status_car = StatusCar(car=car, parking=car.branchoffice)
                status_car.save()
            except IntegrityError:
                messages.add_message(request,
                                     messages.ERROR,
                                     'Ocurrio un terrible error: %s' % car.license_plate)
                return Http404
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'El vehiculo %s se creo correctamente' % car.license_plate)
            return HttpResponseRedirect('/branchoffice/')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Los datos que ingreso son incorrectos')
            return render_to_response('car_form.html', {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = CarToBranchofficeForm()
        return render_to_response('car_form.html', {'form': form},
                                  context_instance=RequestContext(request))

@login_required
def listAllCars(request):
    bo_list = BranchOffice.objects.all()
    cars_list = Car.objects.all()
    return render(request,
                  'list_cars.html',
                  {'cars': cars_list,
                   'bo_list': bo_list})

@login_required
def deleteCar(request, car_id):
    car = Car.objects.get(id=car_id)
    if request.method == 'POST':
        form = CarDeleteForm(request.POST)
        if form.is_valid():
            observation = form.cleaned_data['observation']
            car.is_deleted = True
            car.is_active = False
            car.observation = pickle.dumps({'Item antiguo': car.internal_number,
                               'Placa antigua': car.license_plate,
                               'Ultima observacion': car.observation,
                               'Porque se elimino': observation})
            car.date_end = datetime.date.today()
            car.internal_number = '00x' + car.internal_number
            car.license_plate = '00x' + car.license_plate
            car.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'El vehiculo %s se borro correctamente' % car.internal_number)
            return HttpResponseRedirect('/branchoffice/list/cars/')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Los datos que ingreso son incorrectos')
            return render_to_response('car_delete_form.html',
                                      {'form': form,
                                       'url': car.get_absolute_url(),
                                       'car': car},
                                      context_instance=RequestContext(request))
    else:
        form = CarDeleteForm()
        return render_to_response('car_delete_form.html',
                                  {'form': form,
                                   'url': car.get_absolute_url(),
                                   'car': car},
                                  context_instance=RequestContext(request))

@login_required
def editCar(request, car_id):
    car = Car.objects.get(id=car_id)
    form = CarEditForm(request.POST or None, instance=car)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Los datos se guardaron correctamente')
            return HttpResponseRedirect('/branchoffice/list/cars/')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Revise los datos ingresados')
            return render(request, 'edit_car.html',
                      {'form': form,
                       'url': car.get_absolute_url(),
                       'car': car})
    else:
        return render(request, 'edit_car.html',
                    {'form': form,
                    'url': car.get_absolute_url(),
                    'car': car})

@login_required
def viewCar(request, car_id):
    car = Car.objects.get(id=car_id)
    if car.is_deleted:
        observation = pickle.loads(car.observation)
    else:
        observation = car.observation
    bo_list = BranchOffice.objects.all()
    return render(request, 'view_car.html',
                  {'car': car,
                   'observation': observation,
                   'bo_list': bo_list})

@login_required
def searchByCar(request):
    bo_list = BranchOffice.objects.all()
    if request.method == 'GET':
        internal_number = request.GET['car']
        car = Car.objects.filter(internal_number=internal_number)
        if not car:
            messages.add_message(request,
                                 messages.ERROR,
                                 'El interno del vehiculo no existe: ' + internal_number)
            return HttpResponseRedirect('/branchoffice/list/cars/')
        else:
            return render_to_response('list_cars.html',
                                    {'cars': car,
                                        'bo_list': bo_list},
                                    context_instance=RequestContext(request))

@login_required
def searchByLicensePlate(request):
    bo_list = BranchOffice.objects.all()
    if request.method == 'GET':
        license_plate = request.GET['license_plate']
        car = Car.objects.filter(license_plate=license_plate)
        if not car:
            messages.add_message(request,
                                 messages.ERROR,
                                 'El interno del vehiculo no existe: ' + license_plate)
            return HttpResponseRedirect('/branchoffice/list/cars/')
        else:
            return render_to_response('list_cars.html',
                                    {'cars': car,
                                    'bo_list': bo_list},
                                    context_instance=RequestContext(request))

@login_required
def disabledEnabledCar(request, car_id):
    car = Car.objects.get(id=car_id)
    if car.is_active:
        car.is_active = False
        car.save()
    else:
        m = MaintenanceWorkshop.objects.filter(car=car).filter(fixed=False)
        if m:
            return HttpResponseRedirect(m[0].get_absolute_url() + '/view/')
        else:
            car.is_active = True
            car.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def showCarsByBranchoffice(request, branchoffice_id):
    branchoffice = BranchOffice.objects.get(id=branchoffice_id)
    bo_list = BranchOffice.objects.all()
    cars = Car.objects.filter(branchoffice=branchoffice).filter(is_deleted=False)

    return render_to_response('branchoffice_cars.html',
                              {'cars': cars,
                               'office': branchoffice,
                               'bo_list': bo_list},
                              context_instance=RequestContext(request))

@login_required
def updateCarToBranchoffice(request, branchoffice_id, car_id):
    branchoffice = BranchOffice.objects.get(id=branchoffice_id)
    car = Car.objects.get(id=car_id)
    car.branchoffice = branchoffice
    car.save()
    messages.add_message(request,
                         messages.INFO,
                         'El vehiculo con item ' + car.internal_number + ' se ' +
                         'asigno al parqueo: ' + branchoffice.name)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def showGuardsAll(request):
    guards = GuardsToBranchoffice.objects.all()
    bo_list = BranchOffice.objects.all()
    return render_to_response('branchoffice_guards.html',
                              {'guards': guards,
                               'bo_list': bo_list},
                              context_instance=RequestContext(request))

@login_required
def showGuardsEnabled(request):
    guards = GuardsToBranchoffice.objects.filter(is_active=True)
    bo_list = BranchOffice.objects.all()
    return render_to_response('branchoffice_guards.html',
                              {'guards': guards,
                               'bo_list': bo_list},
                              context_instance=RequestContext(request))

@login_required
def guardInBranchoffice(request, guard_in_office_id):
    gbo = GuardsToBranchoffice.objects.get(id=guard_in_office_id)
    return render(request, 'guard_branchoffice.html', {'guard': gbo})

@login_required
def showGuardsByBranchoffice(request, branchoffice_id):
    branchoffice = BranchOffice.objects.get(id=branchoffice_id)
    bo_list = BranchOffice.objects.all()
    guards = GuardsToBranchoffice.objects.filter(branchoffice=branchoffice).filter(is_active=True)

    return render_to_response('branchoffice_guards.html',
                              {'guards': guards,
                               'office': branchoffice,
                               'bo_list': bo_list},
                              context_instance=RequestContext(request))

@login_required
def updateGuardToBranchoffice(request, branchoffice_id, guard_id):
    branchoffice = BranchOffice.objects.get(id=branchoffice_id)
    guard = Guard.objects.get(id=guard_id)
    try:
        gbo = GuardsToBranchoffice.objects.get(guard=guard)
        gbo.branchoffice = branchoffice
        gbo.save()
    except GuardsToBranchoffice.DoesNotExist:
        gbo = GuardsToBranchoffice(branchoffice=branchoffice,
                                   guard=guard,
                                   date_joined=datetime.date.today(),
                                   observation='Asignado a ' + branchoffice.name)
        gbo.save()
    messages.add_message(request,
                         messages.SUCCESS,
                         'El guardia se asigno correctamente')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def deleteGuardToBranchoffice(request, guard_id):
    guard = Guard.objects.get(id=guard_id)
    gbo = GuardsToBranchoffice.objects.get(guard=guard)
    gbo.is_active = False
    gbo.date_end = datetime.date.today()
    gbo.observation = 'Guardia deshabilitado'
    gbo.save()
    guard.staff.unable()

@login_required
def loadCarToBranchoffice(request):
    reader = xlrd.open_workbook(settings.MEDIA_ROOT + '/'
                                + settings.UPLOAD_PATH + '/files/autos.xls',
                                encoding_override="utf_8")
    sh = reader.sheet_by_name(u'parqueo')

    for rownum in range(sh.nrows):
        #row = sh.row_values(rownum)
        datalist = []
        for i, cell in enumerate(sh.row(rownum)):
            value = cell.value
            datalist.append(value)

            if len(datalist) == 2:
                assignedCarToParking(datalist)
    loadInParking()
    return render(request, 'done.html')

def assignedCarToParking(datalist):
    try:
        parking = BranchOffice.objects.get(name=datalist[1])
    except Exception, err:
        print 'Ocurrio un error'
        print err
        parking = BranchOffice(name=datalist[1])
        parking.save()

    try:
        internal_number = int(datalist[0])
    except ValueError:
        internal_number = datalist[0]
    try:
        car = Car.objects.get(internal_number=internal_number)
        car.branchoffice = parking
        car.save()
        status_car = StatusCar(car=car)
        status_car.parking = parking
        status_car.save()
    except IntegrityError, error:
        print 'error al cargar = ' + error

def loadInParking():
    cars = Car.objects.all()
    for car in cars:
        if car.branchoffice is not None:
            in_parking = InParking(car=car, branchoffice=car.branchoffice)
            in_parking.save()
        else:
            print 'El auto ' + car.internal_number + ' no esta asignado a ningun parqueo'

def uploadCar(request):
    reader = xlrd.open_workbook(settings.MEDIA_ROOT + '/'
                                + settings.UPLOAD_PATH + '/files/autos.xls',
                                encoding_override="utf_8")
    sh = reader.sheet_by_name(u'cars')

    for rownum in range(sh.nrows):
        #row = sh.row_values(rownum)
        datalist = []
        for i, cell in enumerate(sh.row(rownum)):
            value = cell.value
            datalist.append(value)

            if len(datalist) == 11:
                createCar(datalist)
    return render(request, 'done.html')

def createCar(datalist):
    typeCar = getTypeCar(datalist[0])
    cylinder_capacity = int(datalist[7])
    try:
        internal_number = int(datalist[3])
    except ValueError:
        internal_number = datalist[3]
    try:
        car = Car(internal_number=internal_number,
                  type_motorized=typeCar,
                  traction=datalist[1],
                  license_plate=datalist[2],
                  model_year=datalist[5],
                  color=datalist[6],
                  manufacturer=datalist[4],
                  cylinder_capacity=cylinder_capacity,
                  chassis=datalist[8],
                  number_engine=datalist[9],
                  observation=datalist[10])
        car.save()
    except IntegrityError, error:
        print 'Error in car: ' + datalist[2]
        print error

def getTypeCar(typeCar):
    try:
        car = TypeMotorized(name=typeCar)
        car.save()
    except IntegrityError:
        car = TypeMotorized.objects.get(name=typeCar)
    return car

def uploadLadders(request):
    reader = xlrd.open_workbook(settings.MEDIA_ROOT + '/'
                                + settings.UPLOAD_PATH + '/files/autos.xls',
                                encoding_override="utf_8")
    sh = reader.sheet_by_name(u'ladders')

    for rownum in range(sh.nrows):
        #row = sh.row_values(rownum)
        datalist = []
        for i, cell in enumerate(sh.row(rownum)):
            value = cell.value
            datalist.append(value)

            if len(datalist) == 2:
                assignedLadderToCar(datalist)
    return render(request, 'done.html')

def assignedLadderToCar(datalist):
    ladders = re.findall(r"[\w]+", datalist[1])
    try :
        for ladder in ladders:
            l = Ladder(code=ladder)
            l.save()
    except IntegrityError, error:
        print "Error Garrafal de integridad en la base de datos"
        print error

