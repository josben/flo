
from django.shortcuts import render_to_response
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from notifications.forms import NotificationForm, NotificationFromAdminForm
from notifications.models import Notifications
from core.models import User
from staff.models import Staff

@login_required
def notifications(request):
    notifications = Notifications.objects.filter(owner=request.user).order_by('-notification__date_created')
    return render_to_response('notifications.html',
                              {'notifications': notifications},
                              context_instance=RequestContext(request))

@login_required
def myNotifications(request):
    notifications = Notifications.objects.filter(sender=request.user).order_by('-notification__date_created')
    return render_to_response('notifications_sent.html',
                              {'notifications': notifications},
                              context_instance=RequestContext(request))

@login_required
def createNotification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            priority = form.cleaned_data['priority']
            owner = form.cleaned_data['owner']
            notification = form.save()
            notifications = Notifications(priority=priority,
                                          owner=owner,
                                          sender=request.user,
                                          notification=notification)
            notifications.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'La notificacion se envio a %s' % owner)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Los datos que ingreso son incorrectos')
            return render_to_response('notifications_form.html', {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = NotificationForm()
        return render_to_response('notifications_form.html', {'form': form},
                                  context_instance=RequestContext(request))

@login_required
def createNotificationFromAdmin(request):
    if request.method == 'POST':
        form = NotificationFromAdminForm(request.POST)
        if form.is_valid():
            priority = form.cleaned_data['priority']
            owner = form.cleaned_data['owner']
            to_all = form.cleaned_data['to_all']
            only_guard = form.cleaned_data['only_guard']

            notification = form.save()

            if to_all:
                users = User.objects.filter(id__gt=0).filter(is_superuser=False).filter(~Q(username=request.user.username))
                for user in users:
                    notifications = Notifications(priority=priority,
                                                  owner=user,
                                                  sender=request.user,
                                                  notification=notification)
                    notifications.save()
                owner = 'Todos'
            elif only_guard:
                guards = Staff.objects.filter(is_guard=True).filter(is_user=True)
                users = User.objects.filter(staff__in=guards)
                for user in users:
                    notifications = Notifications(priority=priority,
                                                  owner=user,
                                                  sender=request.user,
                                                  notification=notification)
                    notifications.save()
                owner = 'todos los Guardias'

            else:
                notifications = Notifications(priority=priority,
                                                owner=owner,
                                                sender=request.user,
                                                notification=notification)
                notifications.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'La notificacion se envio a %s' % owner)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Los datos que ingreso son incorrectos')
            return render_to_response('notifications_admin_form.html', {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = NotificationFromAdminForm()
        return render_to_response('notifications_admin_form.html', {'form': form},
                                  context_instance=RequestContext(request))

