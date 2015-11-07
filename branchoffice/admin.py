from django.contrib import admin
from .models import (BranchOffice,
                     GuardsToBranchoffice,
                     WorkUnit,
                     EmployeeWorkUnit,
                     TypeMotorized,
                     Car,
                     Ladder)

admin.site.register(BranchOffice)
admin.site.register(GuardsToBranchoffice)
admin.site.register(WorkUnit)
admin.site.register(EmployeeWorkUnit)
admin.site.register(TypeMotorized)
admin.site.register(Car)
admin.site.register(Ladder)

