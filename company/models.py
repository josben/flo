
__author__ = 'Benjamin Perez'

from django.db import models
from django.utils.translation import ugettext as _

class Company(models.Model):
    name = models.CharField(verbose_name=_('company'), max_length=35, unique=True)
    description = models.CharField(verbose_name=_('description'), max_length=450, blank=True, null=True)
    address = models.CharField(verbose_name=_('address'), max_length=450, blank=True, null=True)

    def __unicode__(self):
        return self.name

#class Plant(models.Model):
#    company = models.ForeignKey(Company)
#    address = models.CharField(verbose_name=_('address'), max_length=350, blank=True, null=True)
    
