
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.core.context_processors import csrf
from django.http import HttpResponse

from guest.models import Guest

@login_required
@csrf_protect
def searchGuest(request):
    c = {}
    c.update(csrf(request))
    if request.is_ajax():
        val_document = request.POST.get('val_document', '')
        try:
            guest = Guest.objects.get(val_document=val_document)
            response = TemplateResponse(request,
                                        'ajax_complete_form.html',
                                        {'guest': guest})
            return response
        except Guest.DoesNotExist:
            guest = None
            response = TemplateResponse(request,
                                        'ajax_complete_form.html',
                                        {'guest': guest})
            return response
    else:
        return HttpResponse('<div class="alert fade in alert-danger">' +
                            '    <h4>Ocurrio un error</h4>' +
                            '    Notifique al administrador' +
                            '</div>')


