# encoding: utf-8

from behave import given, when, then
from hamcrest import assert_that, equal_to

class LoginUser(object):
    def __init__(self, uname=None, pwd=None, button=None):
        self.uname = uname
        self.pwd = pwd
        self.button = button

    def login(self):
        assert self.uname is not None
        assert self.pwd is not None
        assert self.button is not None

        if self.button == 'iniciar_sesion':
            return 'Iniciar sesion'
        else:
            return 'Error al ingresar'

class Person(object):
    def __init__(self, type_doc=None, num_doc=None, name=None, city=None, reason=None):
        self.type_doc = type_doc
        self.num_doc = num_doc
        self.name = name
        self.city = city
        self.reason = reason

    def register_person(self):
        assert self.type_doc is not None
        assert self.num_doc is not None
        assert self.name is not None
        assert self.city is not None
        assert self.reason is not None

        return 'Persona registrada'

class RegisterCar(object):
    def __init__(self, internal_number=None, parqueo_out=None, parqueo_in=None, item_out=None, item_in=None,
            km_out=None, km_in=None, escaleras_out=None, escaleras_in=None,
            date_out=None, date_in=None, time_out=None, time_in=None):
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
        self.reg_out = False
        self.reg_in = False

    def validar_salida(self):
        assert self.internal_number is not None
        assert self.parqueo_out is not None
        assert self.item_out is not None
        assert self.km_out is not None
        assert self.escaleras_out is not None
        assert self.date_out is not None
        assert self.time_out is not None

        self.reg_out = True

        return 'Registro guardado'

# Steps: Ingreso al sistema

@given(u'que he introducido mi nombre de usuario {username}')
def step_impl(context, username):
    context.username = username

@given(u'mi contraseña {password}')
def step_impl(context, password):
    context.password = password

@when(u'oprima el boton {button}')
def step_impl(context, button):
    context.button = button
    context.login = LoginUser(context.username, context.password, context.button)

@then(u'debo ingresar al sistema')
def step_impl(context):
    assert_that('Iniciar sesion', equal_to(context.login.login()))

# Steps: Registro de visitas

@given(u'que ingresa una persona con documento {type_doc}')
def step_impl(context, type_doc):
    context.type_doc = type_doc

@given(u'con numero de docuento {num_doc}')
def step_impl(context, num_doc):
    context.num_doc = num_doc

@given(u'con el siguiente nombre {name}')
def step_impl(context, name):
    context.name = name

@given(u'proviene de la ciudad {city}')
def step_impl(context, city):
    context.city = city

@given(u'con el siguinte motivo {reason}')
def step_impl(context, reason):
    context.reason = reason

@when(u'registre a la persona')
def step_impl(context):
    context.person = Person(context.type_doc, context.num_doc, context.name, context.city, context.reason)

@when(u'el {num_doc} sea valido')
def step_impl(context, num_doc):
    assert_that(num_doc, equal_to(context.num_doc))

@then(u'regitro a la persona {name} con documento {num_doc}')
def step_impl(context, name, num_doc):
    assert_that('Persona registrada', equal_to(context.person.register_person()))

# Steps: Registro de salida de vehiculos

@given(u'que sale el vehiculo con numero interno {internal_number}')
def step_impl(context, internal_number):
    context.internal_number = internal_number

@given(u'sale del parqueo {parqueo_out}')
def step_impl(context, parqueo_out):
    context.parqueo_out = parqueo_out

@given(u'con el conductor de salida con item {item_out}')
def step_impl(context, item_out):
    context.item_out = item_out

@given(u'con kilometraje de salida {km_out}')
def step_impl(context, km_out):
    context.km_out = km_out

@given(u'con las escaleras {escaleras_out} de salida')
def step_impl(context, escaleras_out):
    context.escaleras_out = escaleras_out

@given(u'con fecha {date_out} de salida')
def step_impl(context, date_out):
    context.date_out = date_out

@given(u'con hora {time_out} de salida')
def step_impl(context, time_out):
    context.time_out = time_out

@when(u'registre salida del vehiculo {internal_number}')
def step_impl(context, internal_number):
    context.register_car = RegisterCar(internal_number=context.internal_number, parqueo_out=context.parqueo_out, item_out=context.item_out,
            km_out=context.km_out, escaleras_out=context.escaleras_out, date_out=context.date_out, time_out=context.time_out)
    context.car_list = []

@when(u'los datos de salida sean validos')
def step_impl(context):
    assert_that('Registro guardado', equal_to(context.register_car.validar_salida()))

# Steps: Registro de retorno de vehiculos

@given(u'que retorna el vehiculo con numero interno {internal_number}')
def step_impl(context, internal_number):
    for c in context.car_list:
        if c.internal_number == internal_number:
            context.car_tmp = c

@given(u'retorna al parqueo {parqueo_in}')
def step_impl(context, parqueo_in):
    context.car_tmp.parqueo_in = parqueo_in

@given(u'con el conductor de retorno con item {item_in}')
def step_impl(context, item_in):
    context.car_tmp.item_in = item_in

@given(u'con kilometraje de retorno {km_in}')
def step_impl(context, km_in):
    context.car_tmp.km_in = km_in

@given(u'con las escaleras {escaleras_in} de retorno')
def step_impl(context, escaleras_in):
    context.car_tmp.escaleras_in = escaleras_in

@given(u'con fecha {date_in} de retorno')
def step_impl(context, date_in):
    context.car_tmp.date_in = date_in

@given(u'con hora {time_in} de retorno')
def step_impl(context, time_in):
    context.car_tmp.time_in = time_in

@when(u'registre retorno del vehiculo {internal_number}')
def step_impl(context, internal_number):
    assert False

@when(u'los datos del kilometraje sean correctos')
def step_impl(context):
    assert False

@when(u'las escaleras de retorno sean las mismas')
def step_impl(context):
    assert False

@when(u'el conductor sea el mismo')
def step_impl(context):
    assert False

# para ambos: salida y retorno

@when(u'se validen los datos de salida')
def step_impl(context):
    assert_that('Registro guardado', equal_to(context.register_car.validar_salida()))

@then(u'registro al vehiculo {internal_number}')
def step_impl(context, internal_number):
    assert context.register_car.reg_out
    context.car_list.append(context.register_car)


