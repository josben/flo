
from django.contrib import admin
from .models import (CarRegistration,
                     ObservationsRegCar,
                     StatusCar,
                     AllCarRegistration,
                     GuestRegistration,
                     LastDateRegisterByBranchoffice,
                     ForeignCarRegistrationIO)

admin.site.register(CarRegistration)
admin.site.register(ObservationsRegCar)
admin.site.register(StatusCar)
admin.site.register(AllCarRegistration)
admin.site.register(GuestRegistration)
admin.site.register(LastDateRegisterByBranchoffice)
admin.site.register(ForeignCarRegistrationIO)
