# -*- coding: utf-8 -*-

from staff.models import Staff, Employee, Motorist, Guard
from staff.forms import (StaffForm, EmployeeForm,
                         GuardForm, UserForm,
                         MotoristUpdateForm,
                         StaffEditForm)
from branchoffice.models import (WorkUnit, EmployeeWorkUnit,
                                 GuardsToBranchoffice,
                                 TmpWorkUnit, TmpEmployeeWorkUnit)
from core.models import User

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.generic import ListView
#from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.db.utils import IntegrityError

import xlrd
import datetime
import os.path

class EmployeeWorkUnitListView(ListView):
    model = EmployeeWorkUnit
    #queryset = Book.objects.order_by('-publication_date')
    #context_object_name = 'book_list')

@login_required
def index(request):
    staff = Staff.objects.all().order_by('last_name')
    return render_to_response('staff.html', {'staff_list': staff},
            context_instance=RequestContext(request))

@login_required
def editStaff(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    form = StaffEditForm(request.POST or None, request.FILES or None, instance=staff)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request,
                                messages.SUCCESS,
                                'Se guardado correctamente')
            return HttpResponseRedirect(staff.get_absolute_url() + '/detail/')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Revise los datos ingresados, ocurrio un error')
            return render(request, 'edit_staff.html',
                      {'form': form,
                       'staff': staff})
    else:
        return render(request, 'edit_staff.html',
                    {'form': form,
                    'staff': staff})

@login_required
def detailStaff(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    if staff.is_employee:
        e = Employee.objects.get(staff=staff)
        e_wu = EmployeeWorkUnit.objects.get(employee=e)
        return render(request,
                      'detail_staff.html',
                      {'staff': staff, 'employee': e,
                       'e_wu': e_wu})
    elif staff.is_guard:
        g = Guard.objects.get(staff=staff)
        g_bo = GuardsToBranchoffice.objects.get(guard=g)
        return render(request,
                      'detail_staff.html',
                      {'staff': staff, 'guard': g,
                       'g_bo': g_bo})
    else:
        return render(request,
                      'detail_staff.html',
                      {'staff': staff})

@login_required
def listEmployee(request):
    list_employee = EmployeeWorkUnit.objects.all().order_by('employee')

#    paginator = Paginator(staff, 10)
#    page = request.GET.get('page')
#    try:
#        show_lines = paginator.page(page)
#    except PageNotAnInteger:
#        show_lines = paginator.page(1)
#    except EmptyPage:
#        show_lines = paginator.page(paginator.num_pages)

    return render_to_response('list_employee.html', {'staff_list': list_employee},
            context_instance=RequestContext(request))

@login_required
def onlyStaff(request):
    staff = Staff.objects.filter(is_employee=False).filter(is_guard=False).filter(is_user=False)
    return render_to_response('only_staff.html', {'staff_list': staff},
            context_instance=RequestContext(request))

@login_required
def searchStaffByName(request):
    if request.method == 'GET':
        text = request.GET['staff']
        staff = Staff.objects.filter(first_name__icontains=text)
        if not staff:
            messages.add_message(request,
                                 messages.WARNING,
                                 'No se encontro ninguna coincidencia con: '+ text)
            return HttpResponseRedirect('/staff/')
        return render_to_response('staff.html',
                                  {'staff_list': staff},
                                  context_instance=RequestContext(request))

@login_required
def enableDisableStaff(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    if staff.is_active:
        staff.is_active = False
        if staff.is_user:
            user = User.objects.get(staff=staff)
            user.is_active = False
            user.is_admin = False
            user.save()
            staff.is_user = False
        if staff.is_guard:
            guard = Guard.objects.get(staff=staff)
            bo_guard = GuardsToBranchoffice.objects.get(guard=guard)
            bo_guard.is_active = False
            bo_guard.date_end = datetime.date.today()
            bo_guard.save()
        if staff.is_employee:
            employee = Employee.objects.get(staff=staff)
            e_wu = EmployeeWorkUnit.objects.get(employee=employee)
            e_wu.is_active = False
            e_wu.save()
    else:
        staff.is_active = True
        if staff.is_guard:
            guard = Guard.objects.get(staff=staff)
            bo_guard = GuardsToBranchoffice.objects.get(guard=guard)
            bo_guard.is_active = True
            bo_guard.date_joined = datetime.date.today()
            bo_guard.date_end = None
            bo_guard.save()
        if staff.is_employee:
            employee = Employee.objects.get(staff=staff)
            e_wu = EmployeeWorkUnit.objects.get(employee=employee)
            e_wu.is_active = True
            e_wu.save()
    staff.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def getMotorist(request):
    motorist_list = Motorist.objects.all()
    return render_to_response('motorist.html',
                              {'motorist_list': motorist_list},
                              context_instance=RequestContext(request))

@login_required
def updateMotorist(request, motorist_id):
    motorist = Motorist.objects.get(id=motorist_id)
    if request.method == 'POST':
        form = MotoristUpdateForm(request.POST)
        if form.is_valid():
            driver_category = form.cleaned_data['driver_category']
            expiration_date = form.cleaned_data['expiration_date']
            motorist.driver_category = driver_category
            motorist.expiration_date = expiration_date
            motorist.license_is_active = True
            motorist.save()
            return HttpResponseRedirect('/staff/motorist/')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Los datos que ingreso son incorrectos')
            return render(request, 'update_motorist.html',
                          {'form': form, 'url': motorist.get_absolute_url(),
                           'motorist': motorist})
    else:
        form = MotoristUpdateForm()
        return render(request, 'update_motorist.html',
                      {'form': form, 'url': motorist.get_absolute_url(),
                       'motorist': motorist})

@login_required
def searchMotoristByItem(request):
    if request.method == 'GET':
        item = request.GET['item']
        employee = Employee.objects.filter(item=item)
        motorist = Motorist.objects.filter(employee__in=employee)
        if not motorist:
            messages.add_message(request,
                                    messages.ERROR,
                                    'El item %s que ingreso no existe' % item)
            return HttpResponseRedirect('/staff/motorist/')
        return render_to_response('motorist.html', {'motorist_list': motorist},
                                  context_instance=RequestContext(request))

@login_required
def searchMotoristByName(request):
    if request.method == 'GET':
        text = request.GET['employee']
        staff = Staff.objects.filter(first_name__icontains=text)
        employee = Employee.objects.filter(staff__in=staff)
        motorist = Motorist.objects.filter(employee__in=employee)
        if not motorist:
            messages.add_message(request,
                                 messages.WARNING,
                                 'No se encontro ninguna coincidencia con: '+ text)
            return HttpResponseRedirect('/staff/motorist/')
        return render_to_response('motorist.html',
                                  {'motorist_list': motorist},
                                  context_instance=RequestContext(request))

@login_required
def viewProfile(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    user = User.objects.get(staff=staff)
    return HttpResponseRedirect('/accounts/' + str(user.username) + '/')

@login_required
def addUser(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    try:
        user = User.objects.get(staff=staff)
        user.is_active = True
        user.save()
        staff.is_user = True
        staff.save()
        messages.add_message(request,
                             messages.SUCCESS,
                             'El usuario %s se creo correctamente' % user)
        return HttpResponseRedirect('/accounts/' + str(user.username) + '/')
    except User.DoesNotExist:
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                is_admin = form.cleaned_data['is_admin']
                u = User.objects.create_user(email=email,
                                            username=username,
                                            password=password)

                u.save()
                if is_admin:
                    u.is_admin = True
                    u.save()
                u.staff = staff
                u.save()
                staff.is_user = True
                staff.save()
                messages.add_message(request,
                                    messages.SUCCESS,
                                    'El usuario %s se creo correctamente' % u)
                return HttpResponseRedirect('/accounts/' + str(u.username) + '/')
            else:
                messages.add_message(request,
                                    messages.ERROR,
                                    'Los datos que ingreso son incorrectos')
                return render(request, 'create_user.html',
                            {'form': form, 'url': staff.get_absolute_url(),
                            'staff': staff})
        else:
            form = UserForm()
            return render(request, 'create_user.html',
                        {'form': form, 'url': staff.get_absolute_url(),
                        'staff': staff})

@login_required
def addStaff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            staff = form.save()
            type_staff = form.cleaned_data['type_staff']
            if type_staff == 'employee':
                messages.add_message(request,
                                     messages.SUCCESS,
                                     'Se guardo exitosamente, ahora complete' +
                                     ' los datos del personal')
                return HttpResponseRedirect(staff.get_absolute_url() + '/create_employee/')
            else:
                messages.add_message(request,
                                     messages.SUCCESS,
                                     'Se guardo exitosamente, ahora complete' +
                                     ' los datos del guardia')

                return HttpResponseRedirect(staff.get_absolute_url() + '/create_guard/')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Los datos que ingreso son incorrectos')
            return render_to_response('create_staff.html', {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = StaffForm()
        return render_to_response('create_staff.html', {'form': form},
                                  context_instance=RequestContext(request))

@login_required
def addEmployee(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            corporate_number = form.cleaned_data['corporate_number']
            workunit = form.cleaned_data['workunit']
            position = form.cleaned_data['position']
            is_motorist = form.cleaned_data['is_motorist']
            driver_category = form.cleaned_data['driver_category']
            expiration_date = form.cleaned_data['expiration_date']
            employee = Employee(staff=staff,
                                item=item,
                                corporate_number=corporate_number)
            employee.save()
            staff.is_employee = True
            staff.save()
            ewu = EmployeeWorkUnit(employee=employee,
                                   workunit=workunit,
                                   position=position,
                                   date_joined=datetime.datetime.today(),
                                   is_active=True)
            ewu.save()
            if is_motorist:
                me = Motorist(employee=employee,
                              driver_license=employee.staff.val_document,
                              driver_category=driver_category,
                              expiration_date=expiration_date)
                me.save()
                employee.is_motorist = True
                employee.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Se guardo exitosamente al personal')
            return HttpResponseRedirect(employee.get_absolute_url() + '/detail/')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Los datos que ingreso son incorrectos')
            return render(request, 'create_employee.html',
                          {'form': form, 'url': staff.get_absolute_url(),
                           'staff': staff})
    else:
        form = EmployeeForm()
        return render(request, 'create_employee.html',
                      {'form': form, 'url': staff.get_absolute_url(),
                       'staff': staff})

@login_required
def detailEmployee(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    return render(request, 'detail_staff.html',
                 {'employee': employee,
                  'staff': employee.staff})

@login_required
def addGuard(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    if request.method == 'POST':
        form = GuardForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            branchoffice = form.cleaned_data['branchoffice']
            observation = form.cleaned_data['observation']
            guard = Guard(company=company, staff=staff)
            guard.save()
            staff.is_guard = True
            staff.save()
            gb = GuardsToBranchoffice(branchoffice=branchoffice,
                                      guard=guard,
                                      observation=observation)
            gb.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Se creo al guardia exitosamente')
            return HttpResponseRedirect(gb.get_absolute_url() + '/detail/')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Los datos que ingreso son incorrectos')
            return render(request, 'create_guard.html',
                          {'form': form, 'url': staff.get_absolute_url(),
                           'staff': staff})
    else:
        form = GuardForm()
        return render(request, 'create_guard.html',
                      {'form': form, 'url': staff.get_absolute_url(),
                       'staff': staff})

@login_required
def searchByItem(request):
    if request.method == 'GET':
        item = request.GET['item']
        employee = Employee.objects.filter(item=item)
        ewu = EmployeeWorkUnit.objects.filter(employee=employee)
        if not ewu:
            messages.add_message(request,
                                    messages.ERROR,
                                    'El item %s que ingreso no existe' % item)
            return HttpResponseRedirect('/staff/employee/')
        return render_to_response('list_employee.html', {'staff_list': ewu},
                                  context_instance=RequestContext(request))

@login_required
def searchEmployeeByName(request):
    if request.method == 'GET':
        text = request.GET['employee']
        staff = Staff.objects.filter(first_name__icontains=text)
        employee = Employee.objects.filter(staff__in=staff)
        ewu = EmployeeWorkUnit.objects.filter(employee__in=employee)
        if not ewu:
            messages.add_message(request,
                                 messages.WARNING,
                                 'No se encontro ninguna coincidencia con: '+ text)
            return HttpResponseRedirect('/staff/employee/')
        return render_to_response('list_employee.html',
                                  {'staff_list': ewu},
                                  context_instance=RequestContext(request))

@login_required
def uploadDriver(request):
    reader = xlrd.open_workbook(settings.MEDIA_ROOT + '/' + settings.UPLOAD_PATH + '/files/autos.xls',
            encoding_override="utf_8")
    sh = reader.sheet_by_name(u'custodios')

    for rownum in range(sh.nrows):
        #row = sh.row_values(rownum)
        datalist = []
        for i, cell in enumerate(sh.row(rownum)):
            value = cell.value
            if cell.ctype == 3:
                value = datetime.datetime(*xlrd.xldate_as_tuple(value, reader.datemode))
                datalist.append(value.date())
            else:
                datalist.append(value)

            if len(datalist) == 5:
                createDrivers(datalist)
    return render(request, 'done.html')

def createDrivers(datalist):
    try:
        item = int(datalist[1])
        internal_number = int(datalist[0])
    except ValueError:
        internal_number = datalist[0]
    print 'Item = ' + str(item)
    try:
        driver_license = int(datalist[2])
    except ValueError:
        driver_license= datalist[2]

    try:
        employee = Employee.objects.get(item=item)
    except Exception, err:
        print item
        print err

    try:
        is_active = True
        if datalist[4]:
            expiration_date=datalist[4]
            if datetime.date.today() > datalist[4]:
                is_active = False
        else:
            is_active = False
            expiration_date=None
        #if len(driver_license) == 0:
        #    driver_license = None

        try:
            if driver_license == '':
                driver_license = None
            driver = Motorist(employee=employee, driver_license=driver_license, driver_category=datalist[3],
                expiration_date=expiration_date, license_is_active=is_active)
            driver.save()
            employee.is_motorist = True
            employee.save()
        except IntegrityError:
            pass

    except Exception, err:
        print '----------------'
        print datalist
        print 'Error con item = ' + str(item)
        print 'driver_license: ' + str(driver_license)
        print 'category:' + str(datalist[3])
        print 'expiration_date: ' + str(expiration_date)

@login_required
def uploadStaff(request):
    reader = xlrd.open_workbook(settings.MEDIA_ROOT + '/' + settings.UPLOAD_PATH + '/' + 'files/lista_1.xls',
             encoding_override="utf_8")
    sh = reader.sheet_by_name(u'todos')
    for rownum in range(sh.nrows):
        #row = sh.row_values(rownum)
        datalist = []
        for i, cell in enumerate(sh.row(rownum)):
            value = cell.value
            if cell.ctype == 3:
                value = datetime.datetime(*xlrd.xldate_as_tuple(value, reader.datemode))
                datalist.append(value.date())
            else:
                datalist.append(value)
            if len(datalist) == 6:
                createStaff(datalist)
    return render(request, 'done.html')

def createStaff(datalist):
    all_data_user = readAllDataUser(datalist[0], datalist[1], datalist[2], datalist[3], datalist[4], datalist[5])
    loadStaff(all_data_user['staff'], all_data_user['employee'])

def readAllDataUser(item, name, birth_date, ci, cargo, unidad):
    item = int(item)
    myList = name.split()
    size_name = len(myList)
    ci = ci.split()
    num_ci = ci[0]
    locale_ci = ci[1]

    try:
        last_name = myList[0] + " " + myList[1]
        if size_name > 3:
            first_name = myList[2] + " " + myList[3]
        else:
            first_name = myList[2]
    except IndexError:
        last_name = myList[0]
        first_name = myList[1]

    employee = {"item": item, "cargo": cargo, "unidad": unidad}
    path_avatar = settings.PROJECT_ROOT + settings.MEDIA_URL + settings.STAFF_AVATAR_PATH + "/" + str(item) + ".jpg"

    if os.path.exists(path_avatar):
        staff_user = {"first_name": first_name, "last_name": last_name, "ci": num_ci,
                "locale_issue": str(locale_ci).lower(), "birth_date": birth_date, 
                "avatar": settings.STAFF_AVATAR_PATH + "/" + str(item) + ".jpg", 
                "about": 'Trabajador de Comteco'}
    else:
        staff_user = {"first_name": first_name, "last_name": last_name, "ci": num_ci,
                "locale_issue": str(locale_ci).lower(), "birth_date": birth_date,
                "avatar": 'images/default_avatar.png', "about": 'Trabajador de Comteco'}
    return {"staff": staff_user, "employee": employee}

def loadStaff(staff, employee):
#    cargo = createPosition(staff['cargo'])
    unit = createWorkUnit(employee['unidad'])
    try:
        s = Staff(photo=staff['avatar'], first_name=staff['first_name'], last_name=staff['last_name'],
            birth_date=staff['birth_date'], type_document='CI', val_document=staff['ci'],
            locale_issue=staff['locale_issue'], date_joined=datetime.datetime.now(), is_active=True)
        s.save()
    except IntegrityError:
        print 'ERROR GARRAFAL EN USUARIO CON CI: ' + str(staff['ci']) + ' E ITEM: ' + str(employee['item'])

    try:
        e = Employee(staff=s, item=employee['item'])
        e.save()
        wue = EmployeeWorkUnit(employee=e, workunit=unit,
                               position=employee['cargo'],
                               is_active=True)
        wue.save()
    except IntegrityError:
        print 'ERROR AL CARGAR EL ITEM: ' + str(employee['item'])

def createWorkUnit(nameUnit):
    try:
        unit = WorkUnit(name=nameUnit)
        unit.save()
    except IntegrityError:
        unit = WorkUnit.objects.get(name=nameUnit)
    return unit

def moveWorkUnit():
    wu_all = WorkUnit.objects.all()
    for wu in wu_all:
        try:
            tmp_wu = TmpWorkUnit(branchoffice=wu.branchoffice,
                                 name=wu.name,
                                 description=wu.description)
            tmp_wu.save()
        except IntegrityError:
            print 'Ya existe la unidad: ' + str(wu)
    ewu_all = EmployeeWorkUnit.objects.all()
    for ewu in ewu_all:
        try:
            t_wu = TmpWorkUnit.objects.get(name=ewu.workunit.name)
            te_wu = TmpEmployeeWorkUnit(employee=ewu.employee,
                                        workunit=t_wu,
                                        position=ewu.position,
                                        date_joined=ewu.date_joined,
                                        is_active=ewu.is_active)
            te_wu.save()
        except TmpWorkUnit.DoesNotExist:
            print 'Esta unidad no se creo en el paso anterior: ' + str(ewu.workunit)

def repairModels():
    twu_all = TmpWorkUnit.objects.all()
    for twu in twu_all:
        wu = WorkUnit(branchoffice=twu.branchoffice,
                      name=twu.name,
                      description=twu.description)
        wu.save()
    tewu_all = TmpEmployeeWorkUnit.objects.all()
    for tewu in tewu_all:
        try:
            wu = WorkUnit.objects.get(name=tewu.workunit.name)
            ewu = EmployeeWorkUnit(employee=tewu.employee,
                                workunit=wu,
                                position=tewu.position,
                                date_joined=tewu.date_joined,
                                is_active=tewu.is_active)
            ewu.save()
        except WorkUnit.DoesNotExist:
            print 'Esta unidad no se creo: ' + str(tewu.workunit)

def isEmployeGuard():
    e = Employee.objects.all()
    for i in e:
        i.staff.is_employee = True
        i.staff.save()

    g = Guard.objects.all()
    for i in g:
        i.staff.is_guard = True
        i.staff.save()
    print 'done'

