
from django.shortcuts import render, render_to_response
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from .forms import (CarRegistrationForm,
                    GuestSimplifiedForm,
                    CarRegistrationEditForm,
                    ForeignCarRegistrationForm,
                    SelectWorkshopForm)
from .models import (CarRegistration,
                     StatusCar,
                     AllCarRegistration,
                     GuestRegistration,
                     ForeignCarRegistrationIO,
                     LastDateRegisterByBranchoffice)
from staff.models import Guard, Employee
from branchoffice.models import BranchOffice, Car, GuardsToBranchoffice
from maintenance.models import Workshop, MaintenanceWorkshop
from guest.models import Guest

from datetime import timedelta
import itertools
import datetime
import openpyxl
import re

class CarRegistrationUpdate(UpdateView):
    model = CarRegistration
    form_class = CarRegistrationEditForm
#    fields = ['register_time', 'register_km', 'ladders', 'observation']
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        print '====================='
        print form
        print '====================='

def index(request):
    return render(request, 'register.html')

def register(request):
    return render(request, 'register.html')

@login_required
def registerCar(request):
    request.session['today'] = str(datetime.date.today())
    request.session.modified = True
    if request.method == 'POST':
        form = CarRegistrationForm(request, request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            car = form.cleaned_data['car']
            register_date = form.cleaned_data['register_date']
            time = form.cleaned_data['time']
            km = form.cleaned_data['km']
            ladders = form.cleaned_data['ladders']
            observation = form.cleaned_data['observation']

            ######### ESTA SECCION SOLO PERMITE A LOS GUARDIAS REGISTRAR ######
            try:
                guard = Guard.objects.get(staff=request.user.staff)
                branchoffice = GuardsToBranchoffice.objects.filter(guard=guard).filter(is_active=True)
            except Guard.DoesNotExist:
                messages.add_message(request,
                                     messages.ERROR,
                                     'Usted %s no tiene permisos para guadar registros' % request.user.get_full_name())
                return HttpResponseRedirect('/register/register_form/')
            ############### FIN DE LA SECCION ################################

            ############ SECCION PARA MANTENER LA FECHA DE REGISTRO ###########
            if request.POST.get("stick_date"):
                if "stick_date" in request.session:
                    #register_date = request.session["stick_date"]
                    register_date = datetime.datetime.strptime(request.session["stick_date"], "%Y-%m-%d").date()
                else:
                    request.session["stick_date"] = str(register_date)
                    request.session.modified = True
            else:
                if "stick_date" in request.session:
                    del request.session['stick_date']
            ##################### FIN DE ESTA SECCION #########################

            ############# SECCION PARA DISCRIMINAR AUTOS ################
            if car.branchoffice != branchoffice[0].branchoffice:
                messages.add_message(request,
                                        messages.WARNING,
                                        'Este auto pertenece a ' + car.branchoffice.name + '. Use la opcion '+
                                        'de Vehiculos Externos en Opciones')
                return HttpResponseRedirect('/register/register_form/')
            ###################### FIN DE LA SECCION #########################

            status = StatusCar.objects.get(car=car)
            last_register_car = status.last_register_car
            if last_register_car is not None:
                #dt = str(register_date) + ' ' + str(time)
                currentDate = datetime.datetime.combine(register_date, time)
                diff_date = currentDate - last_register_car.register_time
                diff_time = divmod(diff_date.days * 86400 + diff_date.seconds, 60)[0]
                diff_km = km - last_register_car.register_km

                if diff_time <= 60 and diff_km > 80:
                    messages.add_message(request,
                                         messages.ERROR,
                                         'ERROR: No pudo haber recorrido ' +
                                         str(diff_km) + ' km en ' + str(diff_time) + 'minutos')
                    return HttpResponseRedirect('/register/register_form/')
                elif diff_time <= 120 and diff_km > 200:
                    messages.add_message(request,
                                         messages.ERROR,
                                         'ERROR: No pudo haber recorrido ' +
                                         str(diff_km) + ' km en menos de dos horas')
                    return HttpResponseRedirect('/register/register_form/')
                elif diff_time <= 1400 and diff_km >= 1000:
                    messages.add_message(request,
                                         messages.ERROR,
                                         'ERROR: No pudo haber recorrido ' +
                                         str(diff_km) + ' km en menos de un dia')
                    return HttpResponseRedirect('/register/register_form/')

                if str(last_register_car.register_time) > str(register_date) + ' ' + str(time):
                    messages.add_message(request,
                                         messages.ERROR,
                                         'La fecha que ingreso es menor ' +
                                         'que la fecha del ultimo registro.' +
                                         'Ultima fecha: ' + str(last_register_car.register_time) +
                                         'Fecha que ingreso: ' + str(register_date) + ' ' + str(time))
                    return HttpResponseRedirect('/register/register_form/')
                elif str(last_register_car.register_time) == str(register_date) + ' ' + str(time):
                    messages.add_message(request,
                                         messages.ERROR,
                                         'No pudo haber salido al mismo tiempo que ingreso ' + str(time) + ' ' +
                                         'el vehiculo ' + str(car) + ' en fecha ' + str(register_date))
                    return HttpResponseRedirect('/register/register_form/')

                if diff_km < 0:
                    if request.POST.get("km_revert"):
                        car.revert_km = True
                        car.save()
                    else:
                        messages.add_message(request,
                                             messages.ERROR,
                                             'El kilometraje que ingreso es incorrecto, ' +
                                             'es menor que el ultimo registro')
                        return HttpResponseRedirect('/register/register_form/')

            if status.in_moving:
                event = 'entrada'
            else:
                event = 'salida'

            register = CarRegistration(employee=employee, car=car,
                                       branch_office=branchoffice[0].branchoffice,
                                       register_date=register_date,
                                       register_time=datetime.datetime.combine(register_date, time),
                                       register_km=km,
                                       ladders=ladders,
                                       date_modification=datetime.datetime.today(),
                                       event=event,
                                       owner=request.user,
                                       observation=observation)
            register.save()
            status.updateStatus(register)

            ############### section to maintenance #############
            if request.POST.get("maintenance"):
                workshop = Workshop.objects.filter(is_active=True)
                if len(workshop) > 1:
                    return HttpResponseRedirect(register.get_absolute_url() + '/select/workshop/')
                else:
                    if workshop:
                        m = MaintenanceWorkshop(workshop=workshop[0],
                                                car=car,
                                                register=register,
                                                date_joined=register_date,
                                                problem_description=observation,
                                                fixed=False)
                        m.save()
                        car.is_active = False
                        car.save()
                    else:
                        messages.add_message(request,
                                             messages.WARNING,
                                             'No hay ningun taller habilitado, ' +
                                             'el registro se guardo, pero no se ' +
                                             'mando a ningun taller, consulte al ' +
                                             'administrador')
                        return HttpResponseRedirect('/maintenance/workshop/list/')
            else:
                if not car.is_active:
                    m = MaintenanceWorkshop.objects.filter(car=car).filter(fixed=False)[0]
                    m.date_out = register_date
                    m.fixed = True
                    m.save()
                    car.is_active = True
                    car.save()
                    messages.add_message(request,
                                         messages.INFO,
                                         'El vehiculo %s ya se encuentra activo' % car)
            ######## end section maintenance ############

            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Registro guardado exitosamente')
            return HttpResponseRedirect('/register/register_form/')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Ocurrio un error, revise los datos que ingreso')
            if "stick_date" in request.session:
                stick_date = datetime.datetime.strptime(request.session["stick_date"], "%Y-%m-%d")
            else:
                stick_date = ''
            today_date = datetime.date.today()
            return render(request, 'register_form.html', {'form': form,
                                                    'stick_date': stick_date,
                                                    'today': today_date})
    else:
        form = CarRegistrationForm(request)
        if "stick_date" in request.session:
            stick_date = datetime.datetime.strptime(request.session["stick_date"], "%Y-%m-%d")
        else:
            stick_date = ''
        today_date = datetime.date.today()
    return render(request, 'register_form.html', {'form': form,
                                                  'stick_date': stick_date,
                                                  'today': today_date})

@login_required
def registerForeignCar(request):
    request.session['today'] = str(datetime.date.today())
    request.session.modified = True
    if request.method == 'POST':
        form = ForeignCarRegistrationForm(request.POST)
        if form.is_valid():
            event = form.cleaned_data['event']
            employee = form.cleaned_data['employee']
            car = form.cleaned_data['car']
            register_date = form.cleaned_data['register_date']
            time = form.cleaned_data['time']
            km = form.cleaned_data['km']
            ladders = form.cleaned_data['ladders']
            observation = form.cleaned_data['observation']

            ############ SECCION PARA MANTENER LA FECHA DE REGISTRO ###########
            if request.POST.get("stick_date"):
                if "stick_date" in request.session:
                    #register_date = request.session["stick_date"]
                    register_date = datetime.datetime.strptime(request.session["stick_date"], "%Y-%m-%d").date()
                else:
                    request.session["stick_date"] = str(register_date)
                    request.session.modified = True
            else:
                if "stick_date" in request.session:
                    del request.session['stick_date']
            ##################### FIN DE ESTA SECCION #########################
            ######### ESTA SECCION SOLO PERMITE A LOS GUARDIAS REGISTRAR ######
            try:
                guard = Guard.objects.get(staff=request.user.staff)
                branchoffice = GuardsToBranchoffice.objects.filter(guard=guard).filter(is_active=True)
                parking = branchoffice[0].branchoffice
            except Guard.DoesNotExist:
                messages.add_message(request,
                                     messages.ERROR,
                                     'Usted %s no tiene permisos para guadar registros' % request.user.get_full_name())
                return HttpResponseRedirect('/register/foreign_register_form/')
            ############### FIN DE LA SECCION ################################

            ################## SECCION PARA VALIDAR KM #######################
            tmp_register_io = ForeignCarRegistrationIO.objects.filter(car=car).filter(parking=parking)
            if tmp_register_io:
                register_io = tmp_register_io[0].get_last_register()
                if register_io.register_km > km:
                    messages.add_message(request,
                                         messages.ERROR,
                                         'ERROR: El ultimo Kilometraje fue de: ' +
                                         str(register_io.register_km) + ' y usted '
                                         'esta ingresando ' + str(km) + ' que es menor')
                    return HttpResponseRedirect('/register/foreign_register_form/')
                if register_io.register_date > register_date:
                    messages.add_message(request,
                                         messages.ERROR,
                                         'ERROR: La fecha que esta ingresando es menor ' +
                                         'a la fecha del ultimo registro de este ' +
                                         'vehiculo: ' + register_io.register_date.strftime('%Y/%m/%d') +
                                         ' ultima fecha de registro')
                    return HttpResponseRedirect('/register/foreign_register_form/')

            ########################### FIN #################################

            register = CarRegistration(employee=employee, car=car,
                                       branch_office=parking,
                                       register_date=register_date,
                                       register_time=datetime.datetime.combine(register_date, time),
                                       register_km=km,
                                       ladders=ladders,
                                       date_modification=datetime.datetime.today(),
                                       event=event,
                                       owner=request.user,
                                       observation=observation)
            register.save()

            ### Guardamos el registro en TemporalCarRegistrationIO
            #tmp_register_io = ForeignCarRegistrationIO.objects.filter(car=car).filter(parking=parking)
            if tmp_register_io:
                register_io = tmp_register_io[0]
                if event == 'entrada':
                    if register_io.last_event == 'salida':
                        register_io.last_event = event
                        register_io.register_in = register
                        register_io.date_modification = datetime.datetime.today()
                        register_io.save()
                        register_io.verifyRegister()
                    else:
                        register_io.register_in = register
                        register_io.date_modification = datetime.datetime.today()
                        register_io.save()
                else:
                    register_io.register_out = register
                    register_io.last_event = event
                    register_io.date_modification = datetime.datetime.today()
                    register_io.save()
            else:
                if event == 'entrada':
                    tmp_register_io = ForeignCarRegistrationIO(car=car,
                                                               parking=parking,
                                                               register_in=register,
                                                               last_event=event)
                    tmp_register_io.save()
                else:
                    tmp_register_io = ForeignCarRegistrationIO(car=car,
                                                               parking=parking,
                                                               register_out=register,
                                                               last_event=event)
                    tmp_register_io.save()

            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Registro guardado exitosamente')
            return HttpResponseRedirect('/register/foreign_register_form/')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Ocurrio un error, revise los datos que ingreso')
            if "stick_date" in request.session:
                stick_date = datetime.datetime.strptime(request.session["stick_date"], "%Y-%m-%d")
            else:
                stick_date = ''
            today_date = datetime.date.today()

            return render(request, 'register_foreign_form.html', {'form': form,
                                                    'stick_date': stick_date,
                                                    'today': today_date})
#            return HttpResponseRedirect('/register/foreign_register_form/')
    else:
        form = ForeignCarRegistrationForm()
        if "stick_date" in request.session:
            stick_date = datetime.datetime.strptime(request.session["stick_date"], "%Y-%m-%d")
        else:
            stick_date = ''
        today_date = datetime.date.today()

    return render(request, 'register_foreign_form.html', {'form': form,
                                                  'stick_date': stick_date,
                                                  'today': today_date})

@login_required
def registerSimplifiedCar(request):
    if request.method == 'POST':
        form = CarRegistrationForm(request, request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            car = form.cleaned_data['car']
            km = form.cleaned_data['km']
            ladders = form.cleaned_data['ladders']

            status = StatusCar.objects.get(car=car)
            if status.in_moving:
                event = 'entrada'
            else:
                event = 'salida'
            guard = Guard.objects.get(staff=request.user.staff)
            branchoffice = GuardsToBranchoffice.objects.filter(guard=guard).filter(is_active=True)
            register_date = datetime.datetime.today()
            register = CarRegistration(employee=employee, car=car,
                                       branch_office=branchoffice[0].branchoffice,
                                       register_date=register_date,
                                       register_time=register_date,
                                       register_km=km,
                                       ladders=ladders,
                                       date_modification=datetime.datetime.today(),
                                       event=event,
                                       owner=request.user)
            register.save()
            status.updateStatus(register)
            return HttpResponseRedirect('/register/mregister_form/')
    else:
        form = CarRegistrationForm(request)
    return render(request, 'register_simplified_form.html', {'form': form})

@login_required
def registerGuest(request):
    if request.method == 'POST':
        form = GuestSimplifiedForm(request.POST)
        if form.is_valid():
            try:
                guard = Guard.objects.get(staff=request.user.staff)
                branchoffice = GuardsToBranchoffice.objects.filter(guard=guard).filter(is_active=True)
            except Guard.DoesNotExist:
                messages.add_message(request,
                                     messages.ERROR,
                                     'Usted %s no tiene permisos para registrar personas' % request.user)
                return HttpResponseRedirect('/register/guest_form/')

            val_document = form.cleaned_data['val_document']
            reason = form.cleaned_data['reason']

            try:
                guest = Guest.objects.get(val_document=val_document)
            except Guest.DoesNotExist:
                type_document = request.POST.get('type_document')
                city = request.POST.get('city')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                gender = request.POST.get('gender')

                guest = Guest(first_name=first_name,
                              last_name=last_name,
                              type_document=type_document,
                              issue_document=city,
                              val_document=val_document,
                              gender=gender)
                guest.save()

            gr = GuestRegistration(guest=guest,
                                   reason=reason,
                                   branchoffice=branchoffice[0].branchoffice,
                                   owner=request.user)
            gr.save()
            return HttpResponseRedirect('/register/guest_form/')
    else:
        try:
            guard = Guard.objects.get(staff=request.user.staff)
            branchoffice = GuardsToBranchoffice.objects.filter(guard=guard).filter(is_active=True)
            reg_without_exit = GuestRegistration.objects.filter(branchoffice=branchoffice[0].branchoffice).filter(time_out__isnull=True).order_by('-time_entry')
            form = GuestSimplifiedForm()
            return render(request, 'guest_form.html', {'form': form, 'rwe': len(reg_without_exit)})

        except Guard.DoesNotExist:
            messages.add_message(request,
                                    messages.WARNING,
                                    'Usted %s no tiene permisos para registrar personas' % request.user)
            reg_without_exit = GuestRegistration.objects.filter(time_out__isnull=True).order_by('-time_entry')

            form = GuestSimplifiedForm()
        return render(request, 'guest_form.html', {'form': form, 'rwe': len(reg_without_exit)})

            #return HttpResponseRedirect('/')
#        form = GuestSimplifiedForm()
#        reg_without_exit = GuestRegistration.objects.filter(branchoffice=branchoffice).filter(time_out__isnull=True).order_by('-time_entry')
#    return render(request, 'guest_form.html', {'form': form, 'rwe': len(reg_without_exit)})

@login_required
def list_guests(request):
    try:
        guard = Guard.objects.get(staff=request.user.staff)
        gbo = GuardsToBranchoffice.objects.filter(guard=guard).filter(is_active=True)
        bo = gbo[0].branchoffice
    except Guard.DoesNotExist:
        return render_to_response('guest_search_list.html',
                                {'persons': GuestRegistration.objects.order_by('-time_entry'),
                                 'title': 'Ingresos de personas en todas las oficianas'},
                                context_instance = RequestContext(request))
    return render_to_response('guest_list.html',
                              {'persons': GuestRegistration.objects.filter(branchoffice=bo).order_by('-time_entry'),
                               'title': 'Ingreso de personas en ' + bo.name},
                              context_instance = RequestContext(request))

@login_required
def listGuestsToday(request):
    today = datetime.date.today()
    try:
        guard = Guard.objects.get(staff=request.user.staff)
        gbo = GuardsToBranchoffice.objects.filter(guard=guard).filter(is_active=True)
        bo = gbo[0].branchoffice
        guests = GuestRegistration.objects.filter(branchoffice=bo).filter(register_date=today)
        return render_to_response('guest_list.html',
                                {'persons': guests.order_by('-time_entry'),
                                    'title': 'Ingreso de personas, ' + bo.name + ': ' + today.strftime('%d/%m/%y')},
                                context_instance = RequestContext(request))
    except Guard.DoesNotExist:
        guests = GuestRegistration.objects.filter(register_date=today)
        return render_to_response('guest_search_list.html',
                                {'persons': guests.order_by('-time_entry'),
                                 'title': 'Ingresos de personas en todas las oficianas: ' +
                                    today.strftime('%d/%m/%y')},
                                context_instance = RequestContext(request))

@login_required
def listGuestsWithoutExit(request):
    today = datetime.date.today()
    try:
        guard = Guard.objects.get(staff=request.user.staff)
        gbo = GuardsToBranchoffice.objects.filter(guard=guard).filter(is_active=True)
        bo = gbo[0].branchoffice
        guests = GuestRegistration.objects.filter(branchoffice=bo).filter(time_out__isnull=True)
        return render_to_response('guest_list.html',
                                {'persons': guests.order_by('-time_entry'),
                                    'title': 'Ingreso de personas que no se marco su salida en: ' + bo.name},
                                context_instance = RequestContext(request))
    except Guard.DoesNotExist:
        guests = GuestRegistration.objects.filter(time_out__isnull=True)
        return render_to_response('guest_search_list.html',
                                {'persons': guests.order_by('-time_entry'),
                                 'title': 'Ingresos de personas que no se marco su salida'},
                                context_instance = RequestContext(request))

@login_required
def stop_guest(request, register_id):
    gr = GuestRegistration.objects.get(id=register_id)
    gr.register_date = datetime.datetime.today()
    gr.time_out = datetime.datetime.now()
    gr.save()
    if request.is_ajax():
        return HttpResponse(gr.time_out.time().strftime('%H:%M:%S'))
    else:
        return HttpResponseRedirect('/register/persons')

@login_required
def lastRegisters(request):
    today = datetime.date.today()
    end_day = today + timedelta(days=1)
    try:
        guard = Guard.objects.get(staff=request.user.staff)
        bo = GuardsToBranchoffice.objects.filter(guard=guard).filter(is_active=True)
        branchoffice = bo[0].branchoffice

        registers = CarRegistration.objects.filter(
                    branch_office=branchoffice).filter(
                        date_modification__range=(today, end_day))
    except Guard.DoesNotExist:
        registers = CarRegistration.objects.filter(date_modification__range=(today, end_day))
        branchoffice = None

    return render_to_response('list_register_event.html',
                              {'registers': registers.order_by('-date_modification'),
                               'branchoffice': branchoffice,
                               'both': True,
                               'day': today},
                              context_instance = RequestContext(request))

@login_required
def registers_day(request):
    try:
        guard = Guard.objects.get(staff=request.user.staff)
        bo = GuardsToBranchoffice.objects.filter(guard=guard).filter(is_active=True)
        branchoffice = bo[0].branchoffice

        rday = CarRegistration.objects.filter(branch_office=branchoffice).filter(register_date=datetime.datetime.today())
    except Guard.DoesNotExist:
        rday = CarRegistration.objects.filter(register_date=datetime.datetime.today())

    return render_to_response('list_day.html',
                              {'registers': rday.order_by('-register_time'),
                               'branchoffice': branchoffice.name,
                               'day': datetime.datetime.today()},
                              context_instance = RequestContext(request))

@login_required
def registers_all(request):
    try:
        guard = Guard.objects.get(staff=request.user.staff)
        bo = GuardsToBranchoffice.objects.filter(guard=guard).filter(is_active=True)
        branchoffice = bo[0].branchoffice

        rall = AllCarRegistration.objects.filter(parking_out=branchoffice)
    except Guard.DoesNotExist:
        rall = AllCarRegistration.objects.all()
        branchoffice = None

    return render_to_response('list_all.html',
                              {'registers': rall.order_by('-register_date'),
                               'branchoffice': branchoffice},
                              context_instance = RequestContext(request))

@login_required
def registersInput(request):
    try:
        guard = Guard.objects.get(staff=request.user.staff)
        bo = GuardsToBranchoffice.objects.filter(guard=guard).filter(is_active=True)
        branchoffice = bo[0].branchoffice

        rinput = CarRegistration.objects.filter(branch_office=branchoffice).filter(event='entrada')
    except Guard.DoesNotExist:
        rinput = CarRegistration.objects.all().filter(event='entrada')
        branchoffice = None

    return render_to_response('list_register_event.html',
                              {'registers': rinput.order_by('-register_date'),
                               'branchoffice': branchoffice,
                               'event': 'entrada',
                               'both': False},
                              context_instance = RequestContext(request))

@login_required
def registersOutput(request):
    try:
        guard = Guard.objects.get(staff=request.user.staff)
        bo = GuardsToBranchoffice.objects.filter(guard=guard).filter(is_active=True)
        branchoffice = bo[0].branchoffice

        rinput = CarRegistration.objects.filter(branch_office=branchoffice).filter(event='salida')
    except Guard.DoesNotExist:
        rinput = CarRegistration.objects.all().filter(event='salida')
        branchoffice = None

    return render_to_response('list_register_event.html',
                              {'registers': rinput.order_by('-register_date'),
                               'branchoffice': branchoffice,
                               'event': 'salida',
                               'both': False},
                              context_instance = RequestContext(request))

@login_required
def registersBoth(request):
    try:
        guard = Guard.objects.get(staff=request.user.staff)
        bo = GuardsToBranchoffice.objects.filter(guard=guard).filter(is_active=True)
        branchoffice = bo[0].branchoffice

        rinput = CarRegistration.objects.filter(branch_office=branchoffice)
    except Guard.DoesNotExist:
        rinput = CarRegistration.objects.all()
        branchoffice = None

    return render_to_response('list_register_event.html',
                              {'registers': rinput.order_by('-register_date'),
                               'branchoffice': branchoffice,
                               'event': 'both',
                               'both': True},
                              context_instance = RequestContext(request))

@login_required
def searchByCarAndEvent(request):
    if request.method == 'GET':
        try:
            internal_number = request.GET['car']
            event = request.GET['event']
            car = Car.objects.get(internal_number=internal_number)
        except Car.DoesNotExist:
            messages.add_message(request,
                                 messages.ERROR,
                                 'El interno del vehiculo no existe: ' + internal_number)
            if event == 'entrada':
                return HttpResponseRedirect('/register/registers_input/')
            elif event == 'salida':
                return HttpResponseRedirect('/register/registers_output/')
            else:
                return HttpResponseRedirect('/register/registers_both/')

        if event == 'entrada' or event == 'salida':
            list_car = CarRegistration.objects.filter(car=car).filter(event=event).order_by('-register_time')
        else:
            list_car = CarRegistration.objects.filter(car=car).order_by('-register_time')
        return render_to_response('list_register_event.html',
                                  {'registers': list_car,
                                   'event': event},
                                  context_instance=RequestContext(request))

@login_required
def searchByDriverAndEvent(request):
    if request.method == 'GET':
        try:
            item = request.GET['driver']
            event = request.GET['event']
            driver = Employee.objects.get(item=item)
        except Employee.DoesNotExist:
            messages.add_message(request,
                                 messages.ERROR,
                                 'El item ingresado no existe: ' + item)
            if event == 'entrada':
                return HttpResponseRedirect('/register/registers_input/')
            elif event == 'salida':
                return HttpResponseRedirect('/register/registers_output/')
            else:
                return HttpResponseRedirect('/register/registers_both/')

        if event == 'entrada' or event == 'salida':
            list_car = CarRegistration.objects.filter(
                    employee=driver).filter(event=event).order_by('-register_time')
        else:
            list_car = CarRegistration.objects.filter(
                    employee=driver).order_by('-register_time')

        return render_to_response('list_register_event.html',
                                  {'registers': list_car,
                                   'event': event},
                                  context_instance=RequestContext(request))

@login_required
def searchByLadderAndEvent(request):
    if request.method == 'GET':
        ladder = request.GET['ladder']
        event = request.GET['event']
        if event == 'entrada' or event == 'salida':
            list_car = CarRegistration.objects.filter(
                    ladders__contains=ladder).filter(
                            event=event).order_by('-register_time')
        else:
            list_car = CarRegistration.objects.filter(ladders__contains=ladder).order_by('-register_time')

        if not list_car:
            messages.add_message(request,
                                 messages.INFO,
                                 'No se encontro ninguna escalera con el codigo: ' + ladder)
        return render_to_response('list_register_event.html',
                                  {'registers': list_car,
                                   'event': event},
                                  context_instance=RequestContext(request))

@login_required
def editRegisterCar(request, register_id):
    register_car = CarRegistration.objects.get(id=register_id)
    form = CarRegistrationEditForm(request.POST or None, instance=register_car)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Registro guardado correctamente')
            return HttpResponseRedirect(register_car.get_absolute_url() + '/detail/')
#            return HttpResponseRedirect('/register/register_form/')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Revise los datos ingresados: Kilometraje, item, interno del vehiculo')
            return render(request, 'edit_register.html',
                      {'form': form,
                       'url': register_car.get_absolute_url() + '/edit/',
                       'register_id': register_car.id,
                       'employee': register_car.employee,
                       'event': register_car.event,
                       'car': register_car.car})


    else:
        return render(request, 'edit_register.html',
                      {'form': form,
                       'url': register_car.get_absolute_url() + '/edit/',
                       'register_id': register_car.id,
                       'employee': register_car.employee,
                       'event': register_car.event,
                       'car': register_car.car})

@login_required
def detailRegisterCar(request, register_id):
    register = CarRegistration.objects.get(id=register_id)
    return render(request, 'view_register.html',
                  {'register': register})

@login_required
def viewCompleteRegisterCar(request, register_id):
    register = AllCarRegistration.objects.get(id=register_id)
    return render(request, 'complete_register.html',
                  {'register': register})

@login_required
def viewRegisterCar(request, register_id):
    register = CarRegistration.objects.get(id=register_id)
    return render(request, 'view_register.html',
                  {'register': register})

@login_required
def searchByCar(request):
    if request.method == 'GET':
        try:
            internal_number = request.GET['car']
            car = Car.objects.get(internal_number=internal_number)
        except Car.DoesNotExist:
            messages.add_message(request,
                                 messages.ERROR,
                                 'El interno del vehiculo no existe: ' + internal_number)
            return HttpResponseRedirect('/register/registers_all/')
        list_car = AllCarRegistration.objects.filter(car=car).order_by('-time_in')
        return render_to_response('list_all.html', {'registers': list_car},
                                  context_instance=RequestContext(request))

@login_required
def searchByDriver(request):
    if request.method == 'GET':
        try:
            item = request.GET['driver']
            driver = Employee.objects.get(item=item)
        except Employee.DoesNotExist:
            messages.add_message(request,
                                 messages.ERROR,
                                 'El item ingresado no existe: ' + item)
            return HttpResponseRedirect('/register/registers_all/')
        list_car = AllCarRegistration.objects.filter(custody_out=driver).filter(custody_in=driver).order_by('-register_date')
        return render_to_response('list_all.html', {'registers': list_car},
                                  context_instance=RequestContext(request))

@login_required
def searchByLadder(request):
    if request.method == 'GET':
        ladder = request.GET['ladder']
        list_car = AllCarRegistration.objects.filter(ladders_out__contains=ladder).order_by('-register_date')
        if not list_car:
            messages.add_message(request,
                                 messages.INFO,
                                 'No se encontro ninguna escalera con el codigo: ' + ladder)
        return render_to_response('list_all.html', {'registers': list_car},
                                  context_instance=RequestContext(request))

@login_required
def searchByGuest(request):
    if request.method == 'GET':
        text = request.GET['guest']
        persons = Guest.objects.filter(first_name__icontains=text)
        registers = GuestRegistration.objects.filter(guest__in=persons).order_by('-register_date')
        if not registers:
            messages.add_message(request,
                                 messages.INFO,
                                 'No se encontro ninguna coincidencia con: '+ text)
        return render_to_response('guest_search_list.html',
                                  {'persons': registers,
                                   'title': 'Busqueda por: ' + text},
                                  context_instance=RequestContext(request))

@login_required
def searchByCI(request):
    if request.method == 'GET':
        try:
            ci = request.GET['ci']
            person = Guest.objects.get(val_document=ci)
        except Guest.DoesNotExist:
            messages.add_message(request,
                                 messages.INFO,
                                 'No se encontro ningun registro con el documento: ' + ci)
            return HttpResponseRedirect('/register/guests/')
        registers = GuestRegistration.objects.filter(guest=person).order_by('-register_date')

        return render_to_response('guest_search_list.html',
                                  {'persons': registers,
                                   'title': 'Busqueda por: ' + ci},
                                  context_instance=RequestContext(request))

@login_required
def selectByRegisterWorkshop(request, register_id):
    register = CarRegistration.objects.get(id=register_id)
    if request.method == 'POST':
        form = SelectWorkshopForm(request.POST)
        if form.is_valid():
            workshop = form.cleaned_data['workshop']
            m = MaintenanceWorkshop(workshop=workshop,
                                    car=register.car,
                                    register=register,
                                    date_joined=register.register_date,
                                    problem_description=register.observation,
                                    fixed=False)
            m.save()
            register.car.is_active = False
            register.car.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'El vehiculo se mando al taller ' + workshop.branchoffice.name)
            return HttpResponseRedirect('/register/register_form/')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Debe seleccionar un Taller')
            return render(request,
                          'select_workshop.html',
                          {'form': form,
                           'url': register.get_absolute_url() + '/select/workshop/',
                           'car': register.car})
    else:
        form = SelectWorkshopForm()
        return render(request,
                        'select_workshop.html',
                        {'form': form,
                        'url': register.get_absolute_url() + '/select/workshop/',
                        'car': register.car})

#def importOldSystem(request):
def importOldSystem():
    workbook = openpyxl.load_workbook(filename = settings.MEDIA_ROOT + '/'
                                      + settings.UPLOAD_PATH
                                      + '/files/hasta13agosto2014.xlsx',
                                      use_iterators = True)

    worksheet = workbook.get_sheet_by_name('2014')

    for row in worksheet.iter_rows():
        data = {
                'Car': row[0].value,
                'Driver': row[1].value,
                'Date': datetime.datetime.strptime((row[3].value), '%d/%m/%Y').date(),
                'Time out': row[4].value,
                'Km out': row[5].value,
                'Time in': row[6].value,
                'Km in': row[7].value,
                'Ladders': ((', '.join(re.findall(r"[\w]+", row[9].value))) if row[9].value is not None else ''),
        }
        if data['Time in'] is not None:
            loadInDBregister(data, False)
        else:
            loadInDBregister(data, True)
#        loadInDBregister(data)
   # return render(request, 'done.html')
    print 'done.html'

def loadInDBregister(datalist, flag):
    car = Car.objects.get(internal_number=datalist['Car'])
    driver = Employee.objects.get(item=datalist['Driver'])
    parking = BranchOffice.objects.get(name='Muyurina')
    if flag:
        register = AllCarRegistration(car=car,
                                    custody_out=driver,
                                    parking_out=parking,
                                    register_date=datalist['Date'],
                                    time_out=str(datalist['Date']) + ' ' +datalist['Time out'],
                                    km_out=datalist['Km out'],
                                    ladders_out=datalist['Ladders'],
                                    is_complete=False)
    else:
        register = AllCarRegistration(car=car,
                                            custody_out=driver,
                                            custody_in=driver,
                                            parking_out=parking,
                                            parking_in=parking,
                                            register_date=datalist['Date'],
                                            time_out=str(datalist['Date']) + ' ' +datalist['Time out'],
                                            km_out=datalist['Km out'],
                                            time_in=str(datalist['Date']) + ' ' + datalist['Time in'],
                                            km_in=datalist['Km in'],
                                            ladders_out=datalist['Ladders'],
                                            ladders_in=datalist['Ladders'],
                                            is_complete=True)
    register.save()
