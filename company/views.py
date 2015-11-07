
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.template import RequestContext

from company.models import Company
from company.forms import CompanyForm

@login_required
def newCompany(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            description = form.cleaned_data['description']

            company = Company(name=name,
                         address=address,
                         description=description)
            company.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'La empresa %s se creo correctamente' % company.name)
            return HttpResponseRedirect('/staff/only_staff/')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Los datos que ingreso son incorrectos')
            return render_to_response('company_form.html', {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = CompanyForm()
        return render_to_response('company_form.html', {'form': form},
                                  context_instance=RequestContext(request))

