
from staff.models import Staff, Employee, Driver
from utils.models import TypeDocument
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.db.utils import IntegrityError

import xlrd
import datetime
import os.path
import re

@login_required
def index(request):
    staff = Staff.objects.all()

    paginator = Paginator(staff, 10)
    page = request.GET.get('page')
    try:
        show_lines = paginator.page(page)
    except PageNotAnInteger:
        show_lines = paginator.page(1)
    except EmptyPage:
        show_lines = paginator.page(paginator.num_pages)

    return render_to_response('staff.html', {'staff_list': show_lines}, 
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
            driver = Driver(employee=employee, driver_license=driver_license, driver_category=datalist[3],
                expiration_date=expiration_date, is_active=is_active)
            driver.save()
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
#    unit = createWorkUnit(staff['unidad'])
    type_document = TypeDocument.objects.get(key='ci')
    try:
        s = Staff(photo=staff['avatar'], first_name=staff['first_name'], last_name=staff['last_name'],
            birth_date=staff['birth_date'], type_document=type_document, val_document=staff['ci'],
            locale_issue=staff['locale_issue'], date_joined=datetime.datetime.now(), is_active=True)
        s.save()
    except IntegrityError:
        print 'ERROR GARRAFAL EN USUARIO CON CI: ' + str(staff['ci']) + ' E ITEM: ' + str(employee['item'])

    try:
        e = Employee(staff=s, item=employee['item'])
        e.save()
    except IntegrityError:
        print 'ERROR AL CARGAR EL ITEM: ' + employee['item']

"""
def createPosition(nameCargo):
    try:
        cargo = Position(name=nameCargo)
        cargo.save()
    except IntegrityError:
       cargo = Position.objects.get(name=nameCargo)
    return cargo

def createWorkUnit(nameUnit):
    try:
        unit = WorkUnit(name=nameUnit)
        unit.save()
    except IntegrityError:
        unit = WorkUnit.objects.get(name=nameUnit)
    return unit
"""

