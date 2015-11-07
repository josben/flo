from django.shortcuts import render

from notifications.models import Notifications
from accounts.models import ProfileUser

def index(request):
    if request.user.is_authenticated():
        notifications = Notifications.objects.filter(owner=request.user).filter(is_closed=False).order_by('priority')
        profile = ProfileUser.objects.get(user=request.user)
        return render(request,
                      'index.html',
                      {'notifications': notifications,
                       'profile': profile})
    else:
        return render(request, 'index.html', {})

