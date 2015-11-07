
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

