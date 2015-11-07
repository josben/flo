
# encoding: utf-8

from behave import given, when, then
from hamcrest import assert_that, equal_to

import logging

class RegisterCar(object):
    def __init__(self, internal_number=None, parqueo_out=None, parqueo_in=None, item_out=None, item_in=None,
            km_out=None, km_in=None, escaleras_out=None, escaleras_in=None,
            date_out=None, date_in=None, time_out=None, time_in=None, status=None):
        self.internal_number = internal_number
        self.parqueo_out = parqueo_out
        self.parqueo_in = parqueo_in
        self.item_out = item_out
        self.item_in = item_in
        self.km_out = km_out
        self.km_in = km_in
        self.escaleras_out = escaleras_out
        self.escaleras_in = escaleras_in
        self.date_out = date_out
        self.date_in = date_in
        self.time_out = time_out
        self.time_in = time_in
        self.status = status
        self.is_complete = False
        self.there_are_notifications = False
        self.notifications = []

    def validar_salida(self):
        assert self.internal_number is not None
        assert self.parqueo_out is not None
        assert self.item_out is not None
        assert self.km_out is not None
        assert self.escaleras_out is not None
        assert self.date_out is not None
        assert self.time_out is not None

        return 'Registro guardado'

    def validar_retorno(self):
        assert self.parqueo_in is not None
        assert self.item_in is not None
        assert self.km_in is not None
        assert self.escaleras_in is not None
        assert self.date_in is not None
        assert self.time_in is not None

        return 'Registro completo y guardado'

    def validar_escaleras(self):
        if self.escaleras_in != self.escaleras_out:
            self.there_are_notifications = True
            self.notifications.append('OBS: Las escaleras de retorno son diferentes, se guarda el registro con observacion')
            logging.warning('Alerta: Escaleras diferentes')
            return False
        return True

    def validar_conductor(self):
        if self.item_out != self.item_in:
            self.there_are_notifications = True
            self.notifications.append('OBS: El conductor de retorno es diferente, se guarda el registro con observacion')
            logging.warning('Alerta: Conductor diferente')
            return False
        return True

    def validar_parqueo(self):
        if self.parqueo_out != self.parqueo_in:
            self.there_are_notifications = True
            self.notifications.append('OBS: El parqueo de retorno no es el mismo')
            logging.warning('Alerta: El parqueo es diferente')
            return False
        return True

    def validar_km(self):
        if self.km_in < self.km_out:
            message = 'error: El kilometraje de retorno %s es menor que el kilometraje de salida %s' % (self.km_in,self.km_out)
        else:
            message = 'bien'
        return message

def verify(list_out, list_in):
    res = []
    for l in list_in:
        if exist(l, list_out):
            res.append((l, True))
        else:
            res.append((l,False))
    return res

def exist(l, lista):
    for i in lista:
        if i == l:
            return True
    return False

def get_car(cars, internal_number, status):
    if not internal_number in cars:
        return None
    else:
        register = cars.get(internal_number)
        for r in register:
            if not r.is_complete and r.status == 'salida':
                return r
    return None

@given(u'que el vehiculo con numero interno {internal_number} esta de {status}')
def step_impl(context, internal_number, status):
    if not internal_number in context.dict_cars:
        context.internal_number = internal_number
    else:
        registers = context.dict_cars.get(internal_number)
        for register in registers:
            if not register.is_complete and register.status == status:
                logging.error('ERROR: Este vehiculo ya esta de ' + status)
                assert False
            else:
                if not register.is_complete:
                    context.register_car = register
                else:
                    context.internal_number = internal_number
                    assert True

#    car = get_car(context.dict_cars, internal_number, status)
#    if car is not None:
#        context.register_car = car
#    else:
#        context.internal_number = internal_number

@given(u'sale/retorna del parqueo {parqueo}')
def step_impl(context, parqueo):
    if context.register_car is not None:
        context.register_car.parqueo_in = parqueo
    else:
        context.parqueo_out = parqueo

@given(u'con el conductor de con item {item}')
def step_impl(context, item):
    if context.register_car is not None:
        context.register_car.item_in = item
    else:
        context.item_out = item


@given(u'tiene el kilometraje {km}')
def step_impl(context, km):
    if context.register_car is not None:
        context.register_car.km_in = km
        assert_that('bien', equal_to(context.register_car.validar_km()))
    else:
        context.km_out = km

@given(u'con las escaleras {escaleras}')
def step_impl(context, escaleras):
    if context.register_car is not None:
        context.register_car.escaleras_in = escaleras
    else:
        context.escaleras_out = escaleras

@given(u'en fecha {date}')
def step_impl(context, date):
    if context.register_car is not None:
        context.register_car.date_in = date
    else:
        context.date_out = date

@given(u'en horas {time}')
def step_impl(context, time):
    if context.register_car is not None:
        context.register_car.time_in = time
    else:
        context.time_out = time

@when(u'registre al vehiculo {internal_number} con su estado de {status}')
def step_impl(context, internal_number, status):
    if context.register_car is not None:
        context.register_car.is_complete = True
        context.register_car.status = status
    else:
        context.status_car = status
        context.register_car = RegisterCar(internal_number=context.internal_number, parqueo_out=context.parqueo_out,
                item_out=context.item_out, km_out=context.km_out, escaleras_out=context.escaleras_out,
                date_out=context.date_out, time_out=context.time_out, status=context.status_car)

@when(u'los datos del vehiculo {internal_number} sean validos')
def step_impl(context, internal_number):
    if context.register_car.is_complete:
        assert_that('Registro completo y guardado', equal_to(context.register_car.validar_retorno()))
    else:
        assert_that('Registro guardado', equal_to(context.register_car.validar_salida()))

@then(u'guardo el registro del vehiculo {internal_number}')
def step_impl(context, internal_number):
    if not internal_number in context.dict_cars:
        context.dict_cars[internal_number] = [context.register_car]
    else:
        context.dict_cars[internal_number].append(context.register_car)
#    context.list_cars.append(context.register_car)

@then(u'si hay notificaciones se las envia al administrador')
def step_impl(context):
    assert True

@then(u'que pasa si el conductor del vehiculo {internal_number} de retorno es diferente')
def step_impl(context, internal_number):
    if not context.register_car.is_complete:
        context.execute_steps('''
        then si el registro del vehiculo {internal_number} tiene observaciones debe notificarse al supervisor
        '''.format(internal_number=internal_number))
#        assert True
    if context.register_car.is_complete:
        assert context.register_car.validar_conductor()
    else:
        assert True
#    if not context.register_car.validar_conductor():
#        logging.debug('alerta conductor')
#    else:
#        assert True

@then(u'las escaleras del vehiculo {internal_number} de retorno no son las mismas')
def step_impl(context, internal_number):
    context.register_car.validar_escaleras()

@then(u'el parqueo de retorno del vehiculo {internal_number} no es el mismo')
def step_impl(context, internal_number):
    context.register_car.validar_parqueo()

@then(u'si el registro del vehiculo {internal_number} tiene observaciones debe notificarse al supervisor')
def step_impl(context, internal_number):
    if context.register_car.is_complete:
        if context.register_car.there_are_notifications:
            logging.info('Se tienen las siguientes observaciones:')
            for obs in context.register_car.notifications:
                logging.info(obs)
        else:
            assert True

@then(u'envio una alerta al administrador')
def step_impl(context):
    if context.register_car.item_out == context.register_car.item_in:
        assert True
    else:
        logging.warning('Alerta: El conductor de retorno es diferente')
        assert False

# Steps: registro de vehiculos alquilados

@given(u'que tiene la placa de control {placa}')
def step_impl(context, placa):
    assert False

@when(u'registre la salida del vehiculo con placa {placa}')
def step_impl(context, placa):
    assert False

@when(u'registre el retorno del vehiculo con placa {placa}')
def step_impl(context, placa):
    assert False

@when(u'se validen los datos de retorno con los de salida')
def step_impl(context):
    assert False

# Steps para salida y retorno de vehiculos alquilados

@then(u'registro el vehiculo con placa {placa}')
def step_impl(context, placa):
    assert False

