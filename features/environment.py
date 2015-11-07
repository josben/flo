
import logging

def before_all(context):
    context.register_car = None
    context.parqueo_out = None
    context.km_out = None
    context.escaleras_out = None
    context.item_out = None
    context.date_out = None
    context.time_out = None
    context.dict_cars = {}
    context.warning = False

    if not context.config.log_capture:
        logging.basicConfig(level=logging.DEBUG)

