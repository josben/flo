
# encoding: utf-8

from behave import given, when, then

@given(u'que ingreso al sistema con el url "{url}"')
def impl(context, url):
    br = context.browser
    br.visit(url)

@given(u'voy a la opcion "{option}"')
def impl(context, option):
    link = context.browser.find_link_by_text(option).first
    assert link
    link.click()
#    assert option in context.browser.html
#    msg = context.browser.find_link_by_partial_text(option).first
#    assert msg

@given(u'entro con mi nombre de usuario {usr}')
def impl(context, usr):
    context.browser.fill('identification', usr)
    context.user = usr
    assert usr

@given(u'mi contraseña {pwd}')
def impl(context, pwd):
    context.browser.fill('password', pwd)
    context.password = pwd
    assert pwd

@when(u'oprima el boton "{btn}"')
def impl(context, btn):
    button = context.browser.find_by_value(btn).first
    assert button
    button.click()

@then(u'ingreso al sistema y leo el mensaje "{msg}"')
def impl(context, msg):
    assert msg in context.browser.html

@given(u'que vamos a la pagina de registro "{url}"')
def impl(context, url):
    br = context.browser
    br.visit(url)

@given(u'registra el vehiculo con numero interno {car} esta de {status}')
def impl(context, car, status):
    context.browser.fill('car', car)
    context.car = car
    context.status = status

@given(u'sale/retorna del parqueo {parking}')
def impl(context, parking):
    context.parking = parking

@given(u'con el conductor con item {driver}')
def impl(context, driver):
    context.browser.fill('employee', '')
    context.browser.fill('employee', driver)
    context.driver = driver

@given(u'tiene el kilometraje {km}')
def impl(context, km):
    if context.status == 'salida':
        pass
    else:
        #current_km = context.browser.find_by_name('km').first
        #km = int(current_km.value) + 25
        context.browser.fill('km', '')
        context.browser.fill('km', km)

@given(u'con las escaleras {ladders}')
def impl(context, ladders):
    context.browser.fill('ladders', '')
    context.browser.fill('ladders', ladders)

@given(u'en fecha {date}')
def impl(context, date):
    link = context.browser.find_by_id('change_date').first
    assert link
    link.click()
    context.browser.fill('register_date', '')
    context.browser.fill('register_date', date)

@given(u'en horas {time}')
def impl(context, time):
    context.browser.fill('time', '')
    context.browser.fill('time', time)

@when(u'registre al vehiculo {car} con su estado de {status}')
def impl(context, car, status):
    button = context.browser.find_by_value("Registrar").first
    assert button
    button.click()

@when(u'lea el mensaje "{msg}"')
def impl(context, msg):
    assert msg in context.browser.html

@then(u'guardo el registro del vehiculo {car} correctamente')
def impl(context, car):
    pass

