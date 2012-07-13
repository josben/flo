
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Unit(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=140)

    def __unicode__(self):
#        return unicode(self.name_unit)
        return self.name

#    def save(self, *args, **kwargs):
#        super(Unit, self).save(*args, **kwargs)

class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __unicode__(self):
#        return unicode(self.name)
        return self.name

#    def save(self, *args, **kwargs):
#        super(Role, self).save(*args, **kwargs)

class Staff(models.Model):
    SALUDATION_CHOICES = (
        ('1', 'Dr'),
        ('2', 'Sr.'),
        ('3', 'Srta.'),
        ('4', 'Sra.')
    )

    TYPE_DOCUMENT_CHOICES = (
        ('CI', 'Carne de Identidad'),
        ('NI', 'Numero interno'),
    )

    JOB_TITLE_CHOICES = (
        ('1', 'Licenciado'),
        ('2', 'Ingenierio'),
        ('3', 'Tecnico'),
        ('4', 'Sr./Sra.'),
        ('5', 'Bachiller'),
        ('6', 'Estudiante'),
    )

    JOB_ROLE_CHOICES = (
        ('1', 'Gerente'),
        ('2', 'Secretaria'),
        ('3', 'Conductor de vehiculo'),
        ('4', 'Pasante'),
    )

    LOCALE_CHOICES = (
        ('LP', 'La Paz'),
        ('SC', 'Santa Cruz'),
        ('PD', 'Pando'),
        ('BN', 'Beni'),
        ('OR', 'Oruro'),
        ('PT', 'Potosi'),
        ('TJ', 'Tarija'),
        ('CH', 'Chuquisaca'),
        ('CB', 'Cochabamba')
    )

#    user = models.OneToOneField(User, primary_key=True)
    first_name = models.CharField(max_length=50, verbose_name=_(u'Nombre'))
    last_name = models.CharField(max_length=50, verbose_name=_(u'Apellido'))
    type_doc = models.CharField(max_length=2, choices=TYPE_DOCUMENT_CHOICES, verbose_name=(u'Tipo de documento'))
    value_doc = models.CharField(max_length=15, unique=True, verbose_name=(u'Numero de documento'))
    locale_issue = models.CharField(max_length=2, choices=LOCALE_CHOICES, verbose_name=(u'Lugar de expedicion'))

    job_title = models.CharField(max_length=2, choices=JOB_TITLE_CHOICES, verbose_name=_(u'Grado de instruccion'))
    job_role = models.CharField(max_length=2, choices=JOB_ROLE_CHOICES, verbose_name=(u'Cargo'))
    unit = models.ForeignKey(Unit, verbose_name=(u'Unidad'))
    role = models.ForeignKey(Role, verbose_name=(u'Rol'))
    avatar = models.ImageField(upload_to=settings.USER_AVATAR_PATH, null=True,
                               blank=True,
                               max_length=settings.MAX_FILEPATH_LENGTH, verbose_name=(u'Foto'))

#    def __unicode__(self):
#        return unicode(self.id)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        super(Staff, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/staff/%i" % self.id

class Driver(models.Model):
    CATEGORY_CHOICES = (
        ('A', 'Novato'),
        ('B', 'Medio'),
        ('C', 'Experto'),
        ('M', 'Moto')
    )
    staff = models.OneToOneField(Staff, primary_key=True, verbose_name=_(u'Staff'))
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, verbose_name=(u'Categoria'))
    date_issue = models.DateTimeField(_('Fecha de expedicion'))
    date_expiration = models.DateTimeField(_('Fecha de expiracion'))

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return "/driver/%i" % self.id

    def save(self, *args, **kwargs):
        super(Driver, self).save(*args, **kwargs)

"""
class Picture(models.Model):
    register = models.ForeignKey(Register)
    picture = models.ImageField(upload_to='images') #, storage=fs)

    def __unicode__(self):
        return unicode(register)

    def save(self, *args, **kwargs):
        super(Picture, self).save(*args, **kwargs)
"""



"""
    DOCUMENT_CHOICES = (
        ('CI', 'Carne de identidad'),
        ('NI', 'Numero/Codigo interno')
    )

    LOCALE_CHOICES = (
        ('LP', 'La Paz'),
        ('SC', 'Santa Cruz'),
        ('PD', 'Pando'),
        ('BN', 'Beni'),
        ('OR', 'Oruro'),
        ('PT', 'Potosi'),
        ('TJ', 'Tarija'),
        ('CH', 'Chuquisaca'),
        ('CB', 'Cochabamba')
    )
"""

##    first_name = models.CharField(max_length=50)
##    last_name = models.CharField(max_length=50)
#    document = models.ForeignKey(Document)
#    type_license = models.ForeignKey(License)
##    document = models.CharField(max_length=2, choices=DOCUMENT_CHOICES)
##    value_doc = models.IntegerField(max_length=15)
##    locale_issue = models.CharField(max_length=2, choices=LOCALE_CHOICES)
#    staff = models.ForeignKey(Staff)

