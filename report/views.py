
from django.shortcuts import render_to_response, render
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from register.models import (CarRegistration,
                             GuestRegistration,
                             AllCarRegistration)
from maintenance.models import MaintenanceWorkshop, Workshop
from branchoffice.models import BranchOffice, GuardsToBranchoffice, Car
from guest.models import Guest
from staff.models import Motorist

import StringIO
from xlsxwriter.workbook import Workbook


from report.forms import ReportForm
from report.reportPDF import (RegisterCarReportByEvent,
                              RegisterCarReportTogether,
                              RegisterPeopleReport,
                              RegisterWorkshopReport,
                              MotoristReport,
                              GuardsReport,
                              CarsReport)

##### To create report PDF #######
from geraldo.generators import PDFGenerator

@login_required
def report(request):
    if 'csrfmiddlewaretoken' in request.GET:
        form = ReportForm(request.GET)
        if form.is_valid():
            export_to = form.cleaned_data['export_to']
            registers = form.cleaned_data['registers']
            branchoffice = form.cleaned_data['branchoffice']
            report_date = form.cleaned_data['report_date']
            report_date_start = form.cleaned_data['report_date_start']
            report_date_end = form.cleaned_data['report_date_end']
            employee = form.cleaned_data['item_employee']
            car = form.cleaned_data['item_car']
            ci_guest = form.cleaned_data['ci_guest']

            if registers == '1':
                # entrada CarRegistration
                if report_date_start and report_date_end:
                    rp_reg_car = CarRegistration.objects.filter(event='entrada').filter(register_date__range=[report_date_start, report_date_end])
                else:
                    rp_reg_car = CarRegistration.objects.filter(event='entrada').filter(register_date=report_date)
                if branchoffice:
                    rp_reg_car = rp_reg_car.filter(branch_office=branchoffice)
                if car:
                    rp_reg_car = rp_reg_car.filter(car=car)
                if employee:
                    rp_reg_car = rp_reg_car.filter(employee=employee)
                if not rp_reg_car:
                    messages.add_message(request,
                                        messages.WARNING,
                                        'Los datos que ingreso no tienen ningun resultado ' +
                                        'intentelo nuevamene con otros datos. Gracias')
                    return HttpResponseRedirect('/report/')

            elif registers == '2':
                # salida CarRegistration
                if report_date_start and report_date_end:
                    rp_reg_car = CarRegistration.objects.filter(event='salida').filter(register_date__range=[report_date_start, report_date_end])
                else:
                    rp_reg_car = CarRegistration.objects.filter(event='salida').filter(register_date=report_date)
                if branchoffice:
                    rp_reg_car = rp_reg_car.filter(branch_office=branchoffice)
                if car:
                    rp_reg_car = rp_reg_car.filter(car=car)
                if employee:
                    rp_reg_car = rp_reg_car.filter(employee=employee)
                if not rp_reg_car:
                    messages.add_message(request,
                                        messages.WARNING,
                                        'Los datos que ingreso no tienen ningun resultado ' +
                                        'intentelo nuevamene con otros datos. Gracias')
                    return HttpResponseRedirect('/report/')

            elif registers == '3':
                # ambos registers
                if report_date_start and report_date_end:
                    rp_reg_car = CarRegistration.objects.filter(register_date__range=[report_date_start, report_date_end])
                else:
                    rp_reg_car = CarRegistration.objects.filter(register_date=report_date)
                if branchoffice:
                    rp_reg_car = rp_reg_car.filter(branch_office=branchoffice)
                if car:
                    rp_reg_car = rp_reg_car.filter(car=car)
                if employee:
                    rp_reg_car = rp_reg_car.filter(employee=employee)
                if not rp_reg_car:
                    messages.add_message(request,
                                        messages.WARNING,
                                        'Los datos que ingreso no tienen ningun resultado ' +
                                        'intentelo nuevamene con otros datos. Gracias')
                    return HttpResponseRedirect('/report/')

            elif registers == '4':
                # juntos
                if report_date_start and report_date_end:
                    if branchoffice:
                        rp_reg_car_together = AllCarRegistration.objects.filter(parking_out=branchoffice).filter(register_date__range=[report_date_start, report_date_end])
                    else:
                        rp_reg_car_together = AllCarRegistration.objects.filter(register_date__range=[report_date_start, report_date_end])
                else:
                    if branchoffice:
                        rp_reg_car_together = AllCarRegistration.objects.filter(parking_out=branchoffice).filter(register_date=report_date)
                    else:
                        rp_reg_car_together = AllCarRegistration.objects.filter(register_date=report_date)
                if car:
                    rp_reg_car_together = rp_reg_car_together.filter(car=car)
                if employee:
                    rp_reg_car_together = rp_reg_car_together.filter(custody_out=employee)
                if not rp_reg_car_together:
                    messages.add_message(request,
                                        messages.WARNING,
                                        'Los datos que ingreso no tienen ningun resultado ' +
                                        'intentelo nuevamene con otros datos. Gracias')
                    return HttpResponseRedirect('/report/')

            elif registers == '5':
                # personas
                if report_date_start and report_date_end:
                    if branchoffice:
                        rp_guest = GuestRegistration.objects.filter(branchoffice=branchoffice).filter(register_date__range=[report_date_start, report_date_end])
                    else:
                        rp_guest = GuestRegistration.objects.filter(register_date__range=[report_date_start, report_date_end])
                else:
                    if branchoffice:
                        rp_guest = GuestRegistration.objects.filter(branchoffice=branchoffice).filter(register_date=report_date)
                    else:
                        rp_guest = GuestRegistration.objects.filter(register_date=report_date)
                if ci_guest:
                    guest = Guest.objects.get(val_document=ci_guest)
                    rp_guest = rp_guest.filter(guest=guest)
                if not rp_guest:
                    messages.add_message(request,
                                        messages.WARNING,
                                        'Los datos que ingreso no tienen ningun resultado ' +
                                        'intentelo nuevamene con otros datos. Gracias')
                    return HttpResponseRedirect('/report/')

            elif registers == '6':
                # ingresos a taller
                if branchoffice:
                    try:
                        workshop = Workshop.objects.get(branchoffice=branchoffice)
                    except Workshop.DoesNotExist:
                        branchoffice = BranchOffice.objects.get(name='Km. 0')
                        workshop = Workshop.objects.get(branchoffice=branchoffice)
                else:
                    branchoffice = BranchOffice.objects.get(name='Km. 0')
                    workshop = Workshop.objects.get(branchoffice=branchoffice)
                if report_date_start and report_date_end:
                    rp_maintenance = MaintenanceWorkshop.objects.filter(workshop=workshop).filter(date_joined__range=[report_date_start, report_date_end])
                else:
                    rp_maintenance = MaintenanceWorkshop.objects.filter(workshop=workshop).filter(date_joined=report_date)
                if car:
                    rp_maintenance = rp_maintenance.filter(car=car)
                if not rp_maintenance:
                    messages.add_message(request,
                                        messages.WARNING,
                                        'Los datos que ingreso no tienen ningun resultado ' +
                                        'intentelo nuevamene con otros datos. Gracias')
                    return HttpResponseRedirect('/report/')
            elif registers == '7':
                motorist_list = Motorist.objects.all()
            elif registers == '8':
                bo_list = BranchOffice.objects.all()
                gbo_list = GuardsToBranchoffice.objects.filter(is_active=True)
            else:
                if branchoffice:
                    cars_list = Car.objects.filter(branchoffice=branchoffice)
                else:
                    cars_list = Car.objects.all()
                bo_list = BranchOffice.objects.all()

            if export_to == '1':
                if registers == '1':
                    if branchoffice:
                        return render_to_response('list_register_event.html',
                                                  {'registers': rp_reg_car.order_by('register_date'),
                                                   'branchoffice': branchoffice,
                                                   'event': 'entrada',
                                                   'both': False},
                                                  context_instance = RequestContext(request))
                    else:
                        return render_to_response('list_register_event.html',
                                                  {'registers': rp_reg_car.order_by('register_date'),
                                                   'event': 'entrada',
                                                   'both': False},
                                                  context_instance = RequestContext(request))
                elif registers == '2':
                    if branchoffice:
                        return render_to_response('list_register_event.html',
                                                  {'registers': rp_reg_car.order_by('register_date'),
                                                   'branchoffice': branchoffice,
                                                   'event': 'salida',
                                                   'both': False},
                                                  context_instance = RequestContext(request))
                    else:
                        return render_to_response('list_register_event.html',
                                                  {'registers': rp_reg_car.order_by('register_date'),
                                                   'event': 'salida',
                                                   'both': False},
                                                  context_instance = RequestContext(request))
                elif registers == '3':
                    if branchoffice:
                        return render_to_response('list_register_event.html',
                                                  {'registers': rp_reg_car.order_by('register_date'),
                                                   'branchoffice': branchoffice,
                                                   'event': 'both',
                                                   'both': True},
                                                  context_instance = RequestContext(request))
                    else:
                        return render_to_response('list_register_event.html',
                                                  {'registers': rp_reg_car.order_by('register_date'),
                                                   'event': 'both',
                                                   'both': True},
                                                  context_instance = RequestContext(request))
                elif registers == '4':
                    if branchoffice:
                        return render_to_response('list_all.html',
                                                  {'registers': rp_reg_car_together.order_by('register_date'),
                                                   'branchoffice': branchoffice},
                                                  context_instance = RequestContext(request))
                    else:
                        return render_to_response('list_all.html',
                                                  {'registers': rp_reg_car_together.order_by('register_date')},
                                                  context_instance = RequestContext(request))
                elif registers == '5':
                    return render_to_response('guest_list.html',
                                              {'persons': rp_guest.order_by('-time_entry')},
                                              context_instance = RequestContext(request))
                elif registers == '6':
                    return render(request,
                                  'maintenance.html',
                                  {'m_list': rp_maintenance})
                elif registers == '7':
                    return render(request,
                                  'motorist.html',
                                  {'motorist_list': motorist_list})
                elif registers == '8':
                    return render(request,
                                  'branchoffice_guards.html',
                                  {'guards': gbo_list,
                                   'bo_list': bo_list})
                else:
                    return render(request,
                                  'list_cars.html',
                                  {'cars': cars_list,
                                   'bo_list': bo_list})

            elif export_to == '2':
                # EXCEL
                if registers == '1' or registers == '2' or registers == '3':
                    try:
                        output = StringIO.StringIO()
                        book = Workbook(output)
                        sheet = book.add_worksheet('Registro de vehiculos')
                        sheet.write(0, 0, 'Interno de Vehiculo')
                        sheet.write(0, 1, 'Item del conductor')
                        sheet.write(0, 2, 'Conductor del Vehiculo')
                        sheet.write(0, 3, 'Fecha de registro')
                        sheet.write(0, 4, 'Evento')
                        sheet.write(0, 5, 'Hora')
                        sheet.write(0, 6, 'Kilometraje')
                        sheet.write(0, 7, 'Escaleras')

                        i = 1
                        for row in rp_reg_car:
                            sheet.write(i, 0, row.car.internal_number)
                            sheet.write(i, 1, row.employee.item)
                            sheet.write(i, 2, row.employee.staff.full_name())
                            sheet.write(i, 3, row.register_date.strftime('%d/%m/%y'))
                            sheet.write(i, 4, row.event)
                            sheet.write(i, 5, row.register_time.strftime('%H:%M'))
                            sheet.write(i, 6, row.register_km)
                            if row.ladders is None:
                                sheet.write(i, 7, '---')
                            else:
                                sheet.write(i, 7, row.ladders)
                            i+=1
                        book.close()

                        # construct response
                        output.seek(0)
                        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                        response['Content-Disposition'] = "attachment; filename=RegistroDeVehiculos.xlsx"

                        return response
                    except Exception:
                        raise Http404
                elif registers == '4':
                    try:
                        output = StringIO.StringIO()
                        book = Workbook(output)
                        sheet = book.add_worksheet('Registro de vehiculos')
                        sheet.write(0, 0, 'Interno de Vehiculo')
                        sheet.write(0, 1, 'Item del conductor')
                        sheet.write(0, 2, 'Conductor del Vehiculo')
                        sheet.write(0, 3, 'Fecha de registro')
                        sheet.write(0, 4, 'Hora de salida')
                        sheet.write(0, 5, 'Km de salida')
                        sheet.write(0, 6, 'Hora de retorno')
                        sheet.write(0, 7, 'Km de retorno')
                        sheet.write(0, 8, 'Recorrido')
                        sheet.write(0, 9, 'Escaleras')

                        i = 1
                        for row in rp_reg_car_together:
                            sheet.write(i, 0, row.car.internal_number)
                            sheet.write(i, 1, row.custody_out.item)
                            sheet.write(i, 2, row.custody_out.staff.full_name())
                            sheet.write(i, 3, row.register_date.strftime('%d/%m/%y'))
                            sheet.write(i, 4, row.time_out.strftime('%H:%M'))
                            sheet.write(i, 5, row.km_out)
                            if row.time_in is None:
                                sheet.write(i, 6, '')
                            else:
                                sheet.write(i, 6, row.time_in.strftime('%H:%M'))
                            if row.km_in is None:
                                sheet.write(i, 7, '---')
                            else:
                                sheet.write(i, 7, row.km_in)
                            sheet.write(i, 8, row.get_diff_km())
                            sheet.write(i, 9, row.ladders_out)
                            i+=1
                        book.close()

                        # construct response
                        output.seek(0)
                        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                        response['Content-Disposition'] = "attachment; filename=RegistroDeVehiculos.xlsx"

                        return response
                    except Exception:
                        raise Http404
                elif registers == '5':
                    try:
                        output = StringIO.StringIO()
                        book = Workbook(output)
                        sheet = book.add_worksheet('Registro de Personas')
                        sheet.write(0, 0, 'Fecha')
                        sheet.write(0, 1, 'Documento')
                        sheet.write(0, 2, 'Nombre')
                        sheet.write(0, 3, 'Hora de ingreso')
                        sheet.write(0, 4, 'Hora de salida')
                        sheet.write(0, 5, 'Oficina')
                        sheet.write(0, 6, 'Motivo')

                        i = 1
                        for row in rp_guest:
                            sheet.write(i, 0, row.register_date.strftime('%d/%m/%y'))
                            sheet.write(i, 1, row.guest.get_document())
                            sheet.write(i, 2, row.guest.full_name())
                            sheet.write(i, 3, row.time_entry.strftime('%H:%M'))
                            if row.time_out is None:
                                sheet.write(i, 4, '---')
                            else:
                                sheet.write(i, 4, row.time_out.strftime('%H:%M'))
                            sheet.write(i, 5, row.branchoffice.name)
                            if row.reason is None:
                                sheet.write(i, 6, '---')
                            else:
                                sheet.write(i, 6, row.reason)
                            i+=1
                        book.close()

                        # construct response
                        output.seek(0)
                        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                        response['Content-Disposition'] = "attachment; filename=RegistroDePersonas.xlsx"

                        return response
                    except Exception:
                        raise Http404
                elif registers == '6':
                    try:
                        output = StringIO.StringIO()
                        book = Workbook(output)
                        sheet = book.add_worksheet('Registro de Ingresos a Taller')
                        sheet.write(0, 0, 'Taller')
                        sheet.write(0, 1, 'Vehiculo')
                        sheet.write(0, 2, 'Origen')
                        sheet.write(0, 3, 'Conductor de Vehiculo')
                        sheet.write(0, 4, 'Fecha de Ingreso')
                        sheet.write(0, 5, 'Fecha de Salida')
                        sheet.write(0, 6, 'Problema')

                        i = 1
                        for row in rp_maintenance:
                            sheet.write(i, 0, row.workshop.branchoffice.name)
                            sheet.write(i, 1, row.car.internal_number)
                            sheet.write(i, 2, row.register.branch_office.name)
                            sheet.write(i, 3, row.register.employee.staff.full_name())
                            sheet.write(i, 4, row.date_joined.strftime('%d/%m/%y'))
                            if row.date_out is None:
                                sheet.write(i, 5, '---')
                            else:
                                sheet.write(i, 5, row.date_out.strftime('%d/%m/%y'))
                            if row.problem_description is None:
                                sheet.write(i, 6, '---')
                            else:
                                sheet.write(i, 6, row.problem_description)
                            i+=1
                        book.close()

                        # construct response
                        output.seek(0)
                        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                        response['Content-Disposition'] = "attachment; filename=RegistrosTaller.xlsx"

                        return response
                    except Exception:
                        raise Http404
                elif registers == '7':
                    try:
                        output = StringIO.StringIO()
                        book = Workbook(output)
                        sheet = book.add_worksheet('Conductores de Vehiculo')
                        sheet.write(0, 0, 'Item')
                        sheet.write(0, 1, 'Nombre')
                        sheet.write(0, 2, 'CI')
                        sheet.write(0, 3, 'Categoria')
                        sheet.write(0, 4, 'Valides de licencia')

                        i = 1
                        for row in motorist_list:
                            sheet.write(i, 0, row.employee.staff.full_name())
                            sheet.write(i, 1, row.employee.item)
                            sheet.write(i, 2, row.employee.staff.get_document())
                            if row.driver_category is None:
                                sheet.write(i,3, '---')
                            else:
                                sheet.write(i, 3, row.driver_category)
                            if row.expiration_date is None:
                                sheet.write(i, 4, '---')
                            else:
                                sheet.write(i, 4, row.expiration_date.strftime('%d/%m/%y'))
                            i+=1
                        book.close()

                        # construct response
                        output.seek(0)
                        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                        response['Content-Disposition'] = "attachment; filename=Conductores.xlsx"

                        return response
                    except Exception:
                        raise Http404
                elif registers == '8':
                    try:
                        output = StringIO.StringIO()
                        book = Workbook(output)
                        sheet = book.add_worksheet('Conductores de Vehiculo')
                        sheet.write(0, 0, 'Oficina')
                        sheet.write(0, 1, 'CI')
                        sheet.write(0, 2, 'Nombre')
                        sheet.write(0, 3, 'Empresa')
                        sheet.write(0, 4, 'Fecha de ingreso')

                        i = 1
                        for row in gbo_list:
                            sheet.write(i, 0, row.branchoffice.name)
                            sheet.write(i, 1, row.guard.staff.full_name())
                            sheet.write(i, 2, row.guard.staff.get_document())
                            sheet.write(i, 3, row.guard.company.name)
                            sheet.write(i, 4, row.date_joined.strftime('%d/%m/%y'))
                            i+=1
                        book.close()

                        # construct response
                        output.seek(0)
                        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                        response['Content-Disposition'] = "attachment; filename=Guardias.xlsx"
                        return response
                    except Exception, err:
                        raise Http404(err)
                else:
                    try:
                        output = StringIO.StringIO()
                        book = Workbook(output)
                        sheet = book.add_worksheet('Vehiculos de la empresa')
                        sheet.write(0, 0, 'Interno')
                        sheet.write(0, 1, 'Placa')
                        sheet.write(0, 2, 'Chasis')
                        sheet.write(0, 3, 'Tipo')
                        sheet.write(0, 4, 'Modelo')
                        sheet.write(0, 5, 'Marca')
                        sheet.write(0, 6, 'Kilometraje')
                        sheet.write(0, 7, 'Parqueo')

                        i = 1
                        for row in cars_list:
                            sheet.write(i, 0, row.internal_number)
                            sheet.write(i, 1, row.license_plate)
                            if row.chassis is None:
                                sheet.write(i, 2, '---')
                            else:
                                sheet.write(i, 2, row.chassis)
                            if row.type_motorized is None:
                                sheet.write(i, 3, '---')
                            else:
                                sheet.write(i, 3, row.type_motorized.name)
                            if row.model_year is None:
                                sheet.write(i, 4, '---')
                            else:
                                sheet.write(i, 4, row.model_year)
                            if row.manufacturer is None:
                                sheet.write(i, 5, '---')
                            else:
                                sheet.write(i, 5, row.manufacturer)
                            if row.current_km is None:
                                sheet.write(i, 6, '---')
                            else:
                                sheet.write(i, 6, row.current_km)
                            if row.branchoffice is None:
                                sheet.write(i, 7, '---')
                            else:
                                sheet.write(i, 7, row.branchoffice.name)
                            i+=1
                        book.close()

                        # construct response
                        output.seek(0)
                        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                        response['Content-Disposition'] = "attachment; filename=Vehiculos.xlsx"
                        return response
                    except Exception, err:
                        raise Http404(err)
            else:
                # PDF
                if registers == '1' or registers == '2' or registers == '3':
                    try:
                        resp = HttpResponse(content_type='application/pdf')
                        report = RegisterCarReportByEvent(queryset=rp_reg_car)
                        report.title = 'Registro de vehiculos' + ( ' del edificio ' + branchoffice.name if branchoffice is not None else '')
                        report.generate_by(PDFGenerator,filename=resp)
                    except Exception:
                        raise Http404()
                    return resp
                elif registers == '4':
                    try:
                        resp = HttpResponse(content_type='application/pdf')
                        report = RegisterCarReportTogether(queryset=rp_reg_car_together)
                        report.title = 'Registro de vehiculos' + ( ' del edificio ' + branchoffice.name if branchoffice is not None else '')
                        report.generate_by(PDFGenerator,filename=resp)
                    except Exception:
                        raise Http404()
                    return resp
                elif registers == '5':
                    try:
                        resp = HttpResponse(content_type='application/pdf')
                        report = RegisterPeopleReport(queryset=rp_guest)
                        report.title = 'Registro de ingresos de personas' + ( ' del edificio ' + branchoffice.name if branchoffice is not None else '')
                        report.generate_by(PDFGenerator,filename=resp)
                    except Exception:
                        raise Http404()
                    return resp
                elif registers == '6':
                    try:
                        resp = HttpResponse(content_type='application/pdf')
                        report = RegisterWorkshopReport(queryset=rp_maintenance)
                        report.title = 'Registro de ingresos a Taller'
                        report.generate_by(PDFGenerator,filename=resp)
                    except Exception:
                        raise Http404()
                    return resp
                elif registers == '7':
                    try:
                        resp = HttpResponse(content_type='application/pdf')
                        report = MotoristReport(queryset=motorist_list)
                        report.generate_by(PDFGenerator,filename=resp)
                    except Exception:
                        raise Http404()
                    return resp
                elif registers == '8':
                    try:
                        resp = HttpResponse(content_type='application/pdf')
                        report = GuardsReport(queryset=gbo_list)
                        report.generate_by(PDFGenerator,filename=resp)
                    except Exception, err:
                        raise Http404(err)
                    return resp
                else:
                    try:
                        resp = HttpResponse(content_type='application/pdf')
                        report = CarsReport(queryset=cars_list)
                        report.generate_by(PDFGenerator,filename=resp)
                    except Exception, err:
                        raise Http404(err)
                    return resp

            messages.add_message(request,
                                 messages.ERROR,
                                 'ERROR GARRAFAL: No ingreso a ninguna opcion, ' +
                                 'vuelva intentarlo y notifique al administrador ' +
                                 'indicando los datos que ingreso . Gracias')
            return HttpResponseRedirect('/report/')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Los datos que ingreso son incorrectos')
            return render_to_response('report_form.html', {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = ReportForm()
        return render_to_response('report_form.html', {'form': form},
                                  context_instance=RequestContext(request))

