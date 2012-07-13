
from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.staff import models
#from django.core.files.storage import FileSystemStorage

#fs = FileSystemStorage(location=PRIVATE_DIR)

class Register(models.Model):
    CATEGORY_CHOICES = (
        ('A', 'Novato'),
        ('B', 'Medio'),
        ('C', 'Experto'),
        ('M', 'Moto')
    )
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
#    staff = models.OneToOneField(Staff, primary_key=True, verbose_name=_lazy(u'Staff'))
#    document = models.ForeignKey(Document)
#    type_license = models.ForeignKey(License)
##    document = models.CharField(max_length=2, choices=DOCUMENT_CHOICES)
##    value_doc = models.IntegerField(max_length=15)
##    locale_issue = models.CharField(max_length=2, choices=LOCALE_CHOICES)
    staff = models.ForeignKey(Staff)

    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    date_issue = models.DateTimeField(_('Fecha de expedicion'))
    date_expiration = models.DateTimeField(_('Fecha de expiracion'))

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return "/people/%i" % self.id

    def save(self, *args, **kwargs):
        super(Register, self).save(*args, **kwargs)

class Picture(models.Model):
    register = models.ForeignKey(Register)
    picture = models.ImageField(upload_to='images') #, storage=fs)

    def __unicode__(self):
        return unicode(register)

    def save(self, *args, **kwargs):
        super(Picture, self).save(*args, **kwargs)

