
from django.db import models
from django.utils.translation import ugettext as _

ISSUE_CHOICES = (
    ('cba', 'Cochabamba'),
    ('lpz', 'La Paz'),
    ('scz', 'Santa Cruz'),
    ('pnd', 'Pando'),
    ('ben', 'Beni'),
    ('oru', 'Oruro'),
    ('pts', 'Potosi'),
    ('tja', 'Tarija'),
    ('scr', 'Chuquisaca'),
    ('---', _('none')),
    )

GENDER_CHOICES = (
    ('M', _('male')),
    ('F', _('female'))
)

class TypeDocument(models.Model):
    key = models.CharField(max_length=10, unique=True)
    val = models.CharField(max_length=30)
    description = models.CharField(max_length=140, blank=True, null=True)

