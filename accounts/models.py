from django.db import models
from core.models import User

from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile

class ProfileUser(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')
    verified = models.BooleanField(default=True)
    about = models.CharField(max_length=255, blank=True)

