from django.contrib import admin
from .models import Workshop, MaintenanceWorkshop, MaintenanceProgram, MaintenanceCar

admin.site.register(Workshop)
admin.site.register(MaintenanceWorkshop)
admin.site.register(MaintenanceProgram)
admin.site.register(MaintenanceCar)

