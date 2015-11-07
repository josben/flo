
from django.db import models
from django.utils.translation import ugettext as _

from utils.utils import DOCUMENT_CHOICES, ISSUE_CHOICES, GENDER_CHOICES
from staff.models import Employee

class Guest(models.Model):
    first_name = models.CharField(verbose_name=_('first_name'), max_length=45)
    last_name = models.CharField(verbose_name=_('last_name'), max_length=45)
    date_created = models.DateField(auto_now_add=True)
    type_document = models.CharField(max_length=5, choices=DOCUMENT_CHOICES)
    issue_document = models.CharField(verbose_name=_('issue_document'),
                                      max_length=3, 
                                      choices=ISSUE_CHOICES,
                                      blank=True,
                                      null=True)
    val_document = models.CharField(verbose_name=_('val_document'),
                                    max_length=30, unique=True)
    gender = models.CharField(verbose_name=_('gender'),
                              max_length=1,
                              choices=GENDER_CHOICES)
    observation = models.CharField(max_length=300, blank=True, null=True)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_document(self):
        return self.val_document + ' ' + self.issue_document

class BlockGuest(models.Model):
    guest = models.ForeignKey(Guest)
    description = models.CharField(max_length=450)
    date = models.DateTimeField()
    unlock = models.BooleanField(default=False)
    who_unlock = models.ForeignKey(Employee)

