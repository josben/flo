
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from flo.apps.staff.forms import StaffForm, UnitForm, DriverForm, RoleForm
from flo.apps.staff.models import Driver, Staff
#from access.decorators import login_required, logout_required
from django.contrib.auth.decorators import login_required

@login_required
def staff(request):
    print '+++++++++++++++++++++++++++++++++++'
    print request
    print '+++++++++++++++++++++++++++++++++++'
    staff_list = Staff.objects.all()
    print staff_list
    return render_to_response('staff.html', {'staff_list': staff_list}, context_instance = RequestContext(request))

#@ssl_required
#@login_required
#@logout_required
#@require_http_methods(['GET', 'POST'])
@login_required
def register(request):
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
#            first_name = form.cleaned_data['first_name']
#            last_name = form.cleaned_data['last_name']
#            type_doc = form.cleaned_data['type_doc']
#            value_doc = form.cleaned_data['value_doc']
#            locale_issue = form.cleaned_data['locale_issue']
#            job_title = form.cleaned_data['job_title']
#            job_role = form.cleaned_data['job_role']
            staff = form.save()
            return HttpResponseRedirect('/staff/'+ str(staff.id) +'/driver/')
    else:
        form = StaffForm()
    return render(request, 'register.html', {'form': form})

@login_required
def create_unit(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/about/')
    else:
        form = UnitForm()
    return render(request, 'unit.html', {'form': form})

@login_required
def create_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/about/')
    else:
        form = UnitForm()
    return render(request, 'role.html', {'form': form})

@login_required
def register_driver(request, staff_id):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            staff = Staff.objects.get(pk=request.POST['staff'])
            categorypost = form.cleaned_data['category']
            date_issue_post = form.cleaned_data['date_issue']
            date_expiration_post = form.cleaned_data['date_expiration']
            driver = Driver(staff.id, category=categorypost, date_issue=date_issue_post, date_expiration=date_expiration_post)
            driver.save()
            return HttpResponseRedirect('/staff/')
    else:
        form = DriverForm()
    return render(request, 'driver_reg.html', {'form': form, 'staff_id': staff_id})

@login_required
def listing(request):
    staff_list = Staff.objects.all()
    paginator = Paginator(staff_list, 10) # se mostrara 10 por pagina
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    try:
        staff_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        staff_list = paginator.page(paginator.num_pages)

    return render_to_response('list.html', {"staff_list": staff_list})

