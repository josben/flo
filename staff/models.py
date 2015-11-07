
from django.db import models
from django_thumbs.db.models import ImageWithThumbsField
from django.utils.translation import ugettext as _
from django.conf import settings

from utils.utils import DOCUMENT_CHOICES, ISSUE_CHOICES, GENDER_CHOICES
from company.models import Company

class Staff(models.Model):
    first_name = models.CharField(verbose_name=_('first_name'), max_length=45)
    last_name = models.CharField(verbose_name=_('last_name'), max_length=45)
    type_document = models.CharField(max_length=5, choices=DOCUMENT_CHOICES)
    val_document = models.CharField(verbose_name=_('val_document'),
                                    max_length=30, blank=True, null=True,
                                    unique=True)
    locale_issue = models.CharField(verbose_name=_('issue_document'),
                                    max_length=3, choices=ISSUE_CHOICES,
            blank=True, null=True)
    locale_issue_other = models.CharField(verbose_name=_('issue_document_other'),
                                          max_length=45,
            blank=True, null=True)
    birth_date = models.DateField(verbose_name=_('birth_date'),
                                  blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    date_end = models.DateField(blank=True, null=True)
    gender = models.CharField(verbose_name=_('gender'), max_length=1,
                              choices=GENDER_CHOICES, blank=True, null=True)
    photo = ImageWithThumbsField(upload_to=settings.STAFF_AVATAR_PATH,
                                 null=True, blank=True,
                                 verbose_name=_('avatar'),
                                 default='images/default_avatar.png',
                                 sizes=((48,48),(90,90),(200,200),(250,250)))
    about = models.CharField(verbose_name=_('about'), max_length=450,
                             null=True, blank=True)
    number_phone = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_user = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_guard = models.BooleanField(default=False)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    def get_avatar(self):
        return self.photo

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def unable(self):
        self.is_active = False
        self.save()

    def enabled(self):
        self.is_active = True
        self.save()

    def get_absolute_url(self):
        return '/staff/%i' % self.id

    def get_document(self):
        if self.val_document:
            return self.val_document + '-' + self.locale_issue
        else:
            return '---'

class Employee(models.Model):
    staff = models.OneToOneField(Staff, unique=True,
                                 verbose_name=_('employee'),
                                 related_name='Employee')
    item = models.CharField(verbose_name=_('item'),
                            unique=True, max_length=15)
    corporate_number = models.CharField(max_length=30,
                                        unique=True,
                                        blank=True, null=True)
    is_motorist = models.BooleanField(default=False)

    def __unicode__(self):
        return self.staff.full_name()

    def get_motorist(self):
        if self.is_motorist:
            return Motorist.objects.get(employee=self)

    def get_absolute_url(self):
        return '/staff/employee/%i' % self.id

class Motorist(models.Model):
    CATEGORY_CHOICES = (
        ('P', _('category') + ' P'),
        ('A', _('category') + ' A'),
        ('B', _('category') + ' B'),
        ('C', _('category') + ' C'),
        ('M', _('category') + ' M'),
        )

    employee = models.OneToOneField(Employee, unique=True,
                                    verbose_name=_('driver'),
                                    related_name='Driver')
    driver_license = models.CharField(max_length=30,
                                      verbose_name=_('driver_license'),
                                      blank=True, null=True, 
                                      unique=True)
    driver_category = models.CharField(max_length=1, choices=CATEGORY_CHOICES,
                                       verbose_name=_('driver_category'),
                                       blank=True, null=True)
    expiration_date = models.DateField(verbose_name=_('expiration_date'),
                                       blank=True, null=True)
    # this field change with expiration_date
    license_is_active = models.BooleanField()

    def __unicode__(self):
        return self.employee

    def get_absolute_url(self):
        return '/staff/motorist/%i' % self.id

    def get_expiration_date_str(self):
        if self.expiration_date:
            return self.expiration_date.strftime("%d/%m/%y")
        else:
            return '---'

#class Company(models.Model):
#    name = models.CharField(max_length=45)
#    description = models.CharField(max_length=450, blank=True, null=True)

class Guard(models.Model):
    staff = models.OneToOneField(Staff, unique=True, verbose_name=_('guard'),
                                 related_name='Guard')
    company = models.ForeignKey(Company)

    def __unicode__(self):
        return self.staff.full_name()

    def get_absolute_url(self):
        return '/staff/guard/%i' % self.id

