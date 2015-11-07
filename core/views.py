
from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.contrib import messages

from core.models import User
from core.forms import ChangePasswordUserForm

@login_required
@user_passes_test(lambda u: u.is_admin)
def users(request):
    users = User.objects.all()
    return render(request, 'list_users.html', {'users': users})

@login_required
def enableDisableUser(request, user_id):
    user = User.objects.get(id=user_id)
    if user.is_active:
        user.is_active = False
        user.is_admin = False
        if user.staff:
            user.staff.is_user = False
            user.staff.save()
        messages.add_message(request,
                             messages.SUCCESS,
                             'El usuario %s se deshabilitado' % user)
    else:
        user.is_active = True
        if user.staff:
            user.staff.is_user = True
            user.staff.is_active = True
            user.staff.save()
        messages.add_message(request,
                             messages.SUCCESS,
                             'El usuario %s se habilitado' % user)
    user.save()
    return HttpResponseRedirect('/core/users/')

@login_required
def isAdminUser(request, user_id):
    user = User.objects.get(id=user_id)
    if user.is_admin:
        user.is_admin = False
        messages.add_message(request,
                             messages.SUCCESS,
                             'El usuario %s ya no es admin' % user)
    else:
        user.is_admin = True
        messages.add_message(request,
                             messages.SUCCESS,
                             'El usuario %s es admin' % user)
    user.save()
    return HttpResponseRedirect('/core/users/')

@login_required
def changePasswordUser(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = ChangePasswordUserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'El usuario %s tiene nuevo password' % user)
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Los datos que ingreso son incorrectos')
            return render(request, 'change_password.html',
                          {'form': form, 'url': user.get_absolute_url(),
                           'user': user})
    else:
        form = ChangePasswordUserForm()
        return render(request, 'change_password.html',
                      {'form': form, 'url': user.get_absolute_url(),
                       'user': user})
    return HttpResponseRedirect('/core/users/')

