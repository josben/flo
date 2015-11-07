
# encoding: utf-8

from behave import given, when, then

import logging

class Mantenimiento(object):
    def __init__(self, internal_number, km_last_maintenance,
                 current_km, next_km_maintenance, mantenimiento=False):
        self.internal_number = internal_number
        self.km_last_maintenance = km_last_maintenance
        self.current_km = current_km
        self.next_km_maintenance = next_km_maintenance
        self.mantenimiento = mantenimiento

    def asignarMantenimiento(self):
        diff = int(self.current_km) - int(self.next_km_maintenance)
        if diff >= 200:
            self.mantenimiento = True

@given(u'el vehiculo {internal_number}')
def step_impl(context, internal_number):
    context.internal_number = internal_number

@given(u'el kilometraje del ultimo mantenimiento fue {km_last_maintenance}')
def step_impl(context, km_last_maintenance):
    context.km_last_maintenance = km_last_maintenance

@given(u'su siguiente mantenimiento es {next_km_maintenance}')
def step_impl(context, next_km_maintenance):
    context.next_km_maintenance = next_km_maintenance

@given(u'el kilometraje actual es {current_km}')
def step_impl(context, current_km):
    context.current_km = current_km

@when(u'los datos son analizados')
def step_impl(context):
    context.mantenimiento = Mantenimiento(context.internal_number,
                                          context.km_last_maintenance,
                                          context.next_km_maintenance,
                                          context.current_km)

    context.mantenimiento.asignarMantenimiento()

@then(u'se asigna el vehiculo para mantenimiento')
def step_impl(context):
    if context.mantenimiento.mantenimiento:
        logging.info("SE ASIGNA PARA MANTENIMIENTO")
    else:
        assert context.mantenimiento.mantenimiento
        logging.info("NO SE HACE NADA")


