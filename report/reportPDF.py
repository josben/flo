
import os
cur_dir = os.path.dirname(os.path.abspath(__file__))

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

from geraldo import Report, ReportBand, Label, ObjectValue, SystemField, landscape, \
    FIELD_ACTION_COUNT, BAND_WIDTH

class RegisterCarReportByEvent(Report):
    title = 'Registro de Vehiculos'
#    page_size = letter
    page_size = landscape(letter)

#    class band_begin(ReportBand):
#        height = 1*cm
#        elements = [
#            Label(text='Registro de Vehiculos de un rango de fechas', top=0.1*cm,
#                left=8*cm),
#        ]

    class band_summary(ReportBand):
        height = 0.7*cm
        elements = [
            Label(text="En total", top=0.1*cm, left=0),
            ObjectValue(attribute_name='id', top=0.1*cm, left=3*cm,
                action=FIELD_ACTION_COUNT,
                display_format='%s registros encontrados'),
        ]
        borders = {'all': True}

    class band_page_header(ReportBand):
        height = 1.3*cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1*cm,
                left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold',
                'fontSize': 14, 'alignment': TA_CENTER}),
            Label(text="Interno", top=0.8*cm, left=0),
            Label(text="Item", top=0.8*cm, left=1.5*cm),
            Label(text="Chofer", top=0.8*cm, left=3*cm),
            Label(text="Fecha", top=0.8*cm, left=9*cm),
            Label(text="Event", top=0.8*cm, left=11.3*cm),
            Label(text="Hora", top=0.8*cm, left=13*cm),
            Label(text="Kilometraje", top=0.8*cm, left=15*cm),
            Label(text="Escaleras", top=0.8*cm, left=17*cm),
        ]
        borders = {'bottom': True}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='Reporte de la unidad', top=0.1*cm, left=0),
            SystemField(expression='Pagina # %(page_number)d de %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
        ]
        borders = {'top': True}

    class band_detail(ReportBand):
        height = 0.5*cm
        elements = [
            ObjectValue(attribute_name='car', top=0, left=0),
            ObjectValue(attribute_name='employee.item', top=0, left=1.5*cm, width=7*cm),
            ObjectValue(attribute_name='employee.staff.full_name', top=0, left=3*cm, width=7*cm),
            ObjectValue(attribute_name='get_date_str', top=0, left=9*cm, width=7*cm),
            ObjectValue(attribute_name='event', top=0, left=11.3*cm, width=7*cm),
            ObjectValue(attribute_name='register_time.time', top=0, left=13*cm, width=7*cm),
            ObjectValue(attribute_name='register_km', top=0, left=15*cm, width=7*cm),
            ObjectValue(attribute_name='ladders', top=0, left=17*cm, width=7*cm),
        ]

class RegisterCarReportTogether(Report):
    title = 'Registro de Vehiculos'
#    page_size = letter
    page_size = landscape(letter)

#    class band_begin(ReportBand):
#        height = 1*cm
#        elements = [
#            Label(text='Registro de Vehiculos de un rango de fechas', top=0.1*cm,
#                left=8*cm),
#        ]

    class band_summary(ReportBand):
        height = 0.7*cm
        elements = [
            Label(text="En total", top=0.1*cm, left=0),
            ObjectValue(attribute_name='id', top=0.1*cm, left=3*cm,
                action=FIELD_ACTION_COUNT,
                display_format='%s registros encontrados'),
        ]
        borders = {'all': True}

    class band_page_header(ReportBand):
        height = 1.3*cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1*cm,
                left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold',
                'fontSize': 14, 'alignment': TA_CENTER}),
            Label(text="Interno", top=0.8*cm, left=0),
            Label(text="Item", top=0.8*cm, left=1.5*cm),
            Label(text="Chofer", top=0.8*cm, left=3*cm),
            Label(text="Fecha", top=0.8*cm, left=9*cm),
            Label(text="Hr salida", top=0.8*cm, left=11.3*cm),
            Label(text="Km salida", top=0.8*cm, left=13*cm),
            Label(text="Hr retorno", top=0.8*cm, left=15*cm),
            Label(text="Km retorno", top=0.8*cm, left=17*cm),
            Label(text="Recorrido", top=0.8*cm, left=19*cm),
            Label(text="Escaleras", top=0.8*cm, left=21*cm),
        ]
        borders = {'bottom': True}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='Reporte de la unidad', top=0.1*cm, left=0),
            SystemField(expression='Pagina # %(page_number)d de %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
        ]
        borders = {'top': True}

    class band_detail(ReportBand):
        height = 0.5*cm
        elements = [
            ObjectValue(attribute_name='car', top=0, left=0),
            ObjectValue(attribute_name='custody_out.item', top=0, left=1.5*cm, width=7*cm),
            ObjectValue(attribute_name='custody_out.staff.full_name', top=0, left=3*cm, width=7*cm),
            ObjectValue(attribute_name='get_date_str', top=0, left=9*cm, width=7*cm),
            ObjectValue(attribute_name='time_out.time', top=0, left=11.3*cm, width=7*cm),
            ObjectValue(attribute_name='km_out', top=0, left=13*cm, width=7*cm),
            ObjectValue(attribute_name='get_time_in_str', top=0, left=15*cm, width=7*cm),
            ObjectValue(attribute_name='km_in', top=0, left=17*cm, width=7*cm),
            ObjectValue(attribute_name='get_diff_km', top=0, left=19*cm, width=7*cm),
            ObjectValue(attribute_name='ladders_out', top=0, left=21*cm, width=7*cm),
        ]

class RegisterPeopleReport(Report):
    title = 'Registro de ingreso de Personas'
#    page_size = letter
    page_size = landscape(letter)

#    class band_begin(ReportBand):
#        height = 1*cm
#        elements = [
#            Label(text='Registro de Vehiculos de un rango de fechas', top=0.1*cm,
#                left=8*cm),
#        ]

    class band_summary(ReportBand):
        height = 0.7*cm
        elements = [
            Label(text="En total", top=0.1*cm, left=0),
            ObjectValue(attribute_name='id', top=0.1*cm, left=3*cm,
                action=FIELD_ACTION_COUNT,
                display_format='%s registros encontrados'),
        ]
        borders = {'all': True}

    class band_page_header(ReportBand):
        height = 1.3*cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1*cm,
                left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold',
                'fontSize': 14, 'alignment': TA_CENTER}),
            Label(text="Fecha", top=0.8*cm, left=0),
            Label(text="CI", top=0.8*cm, left=2*cm),
            Label(text="Nombre", top=0.8*cm, left=5*cm),
            Label(text="Ingreso", top=0.8*cm, left=12*cm),
            Label(text="Salida", top=0.8*cm, left=13.9*cm),
            Label(text="Oficina", top=0.8*cm, left=16.5*cm),
            Label(text="Motivo", top=0.8*cm, left=18.5*cm),
        ]
        borders = {'bottom': True}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='Reporte de la unidad', top=0.1*cm, left=0),
            SystemField(expression='Pagina # %(page_number)d de %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
        ]
        borders = {'top': True}

    class band_detail(ReportBand):
        height = 2.1*cm
        auto_expand_height = True
        margin_bottom = 0.4*cm
        elements = [
            ObjectValue(attribute_name='get_date_str', top=0, left=0),
            ObjectValue(attribute_name='guest.get_document', top=0, left=2*cm, width=7*cm),
            ObjectValue(attribute_name='guest', top=0, left=5*cm, width=7*cm),
            ObjectValue(attribute_name='time_entry.time', top=0, left=12*cm, width=7*cm),
            ObjectValue(attribute_name='get_time_out_str', top=0, left=13.9*cm, width=7*cm),
            ObjectValue(attribute_name='branchoffice', top=0, left=16.5*cm, width=7*cm),
            ObjectValue(attribute_name='reason', top=0, left=18.5*cm, width=7*cm),
        ]

class RegisterWorkshopReport(Report):
    title = 'Registro de ingresos a Taller'
#    page_size = letter
    page_size = landscape(letter)

#    class band_begin(ReportBand):
#        height = 1*cm
#        elements = [
#            Label(text='Registro de Vehiculos de un rango de fechas', top=0.1*cm,
#                left=8*cm),
#        ]

    class band_summary(ReportBand):
        height = 0.7*cm
        elements = [
            Label(text="En total", top=0.1*cm, left=0),
            ObjectValue(attribute_name='id', top=0.1*cm, left=3*cm,
                action=FIELD_ACTION_COUNT,
                display_format='%s registros encontrados'),
        ]
        borders = {'all': True}

    class band_page_header(ReportBand):
        height = 1.3*cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1*cm,
                left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold',
                'fontSize': 14, 'alignment': TA_CENTER}),
            Label(text="Taller", top=0.8*cm, left=0),
            Label(text="Vehiculo", top=0.8*cm, left=2*cm),
            Label(text="Conductor", top=0.8*cm, left=4*cm),
            Label(text="Oficina", top=0.8*cm, left=10*cm),
            Label(text="Ingreso", top=0.8*cm, left=12*cm),
            Label(text="Salida", top=0.8*cm, left=13.9*cm),
            Label(text="Problema", top=0.8*cm, left=16.5*cm),
        ]
        borders = {'bottom': True}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='Reporte de la unidad', top=0.1*cm, left=0),
            SystemField(expression='Pagina # %(page_number)d de %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
        ]
        borders = {'top': True}

    class band_detail(ReportBand):
        height = 2.1*cm
        auto_expand_height = True
        margin_bottom = 0.4*cm
        elements = [
            ObjectValue(attribute_name='workshop', top=0, left=0),
            ObjectValue(attribute_name='car', top=0, left=2*cm, width=7*cm),
            ObjectValue(attribute_name='register.employee.staff.full_name', top=0, left=4*cm, width=7*cm),
            ObjectValue(attribute_name='register.branch_office', top=0, left=10*cm, width=7*cm),
            ObjectValue(attribute_name='get_date_joined_str', top=0, left=12*cm, width=7*cm),
            ObjectValue(attribute_name='get_date_out_str', top=0, left=13.9*cm, width=7*cm),
            ObjectValue(attribute_name='problem_description', top=0, left=16.5*cm, width=7*cm),
        ]

class MotoristReport(Report):
    title = 'Reporte de la unidad'
#    page_size = letter
    page_size = landscape(letter)

#    class band_begin(ReportBand):
#        height = 1*cm
#        elements = [
#            Label(text='Registro de Vehiculos de un rango de fechas', top=0.1*cm,
#                left=8*cm),
#        ]

    class band_summary(ReportBand):
        height = 0.7*cm
        elements = [
            Label(text="En total", top=0.1*cm, left=0),
            ObjectValue(attribute_name='id', top=0.1*cm, left=3*cm,
                action=FIELD_ACTION_COUNT,
                display_format='%s registros encontrados'),
        ]
        borders = {'all': True}

    class band_page_header(ReportBand):
        height = 1.3*cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1*cm,
                left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold',
                'fontSize': 14, 'alignment': TA_CENTER}),
            Label(text="Item", top=0.8*cm, left=0),
            Label(text="Nombre", top=0.8*cm, left=2*cm),
            Label(text="CI", top=0.8*cm, left=9*cm),
            Label(text="Categoria", top=0.8*cm, left=13*cm),
            Label(text="Valides de licencia", top=0.8*cm, left=17*cm),
        ]
        borders = {'bottom': True}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='Reporte de la unidad', top=0.1*cm, left=0),
            SystemField(expression='Pagina # %(page_number)d de %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
        ]
        borders = {'top': True}

    class band_detail(ReportBand):
        height = 2.1*cm
        auto_expand_height = True
        margin_bottom = 0.4*cm
        elements = [
            ObjectValue(attribute_name='employee.item', top=0, left=0),
            ObjectValue(attribute_name='employee.staff.full_name', top=0, left=2*cm, width=7*cm),
            ObjectValue(attribute_name='employee.staff.get_document', top=0, left=9*cm, width=7*cm),
            ObjectValue(attribute_name='driver_category', top=0, left=13*cm, width=7*cm),
            ObjectValue(attribute_name='get_expiration_date_str', top=0, left=17*cm, width=7*cm),
        ]

class GuardsReport(Report):
    title = 'Guardias'
#    page_size = letter
    page_size = landscape(letter)

#    class band_begin(ReportBand):
#        height = 1*cm
#        elements = [
#            Label(text='Registro de Vehiculos de un rango de fechas', top=0.1*cm,
#                left=8*cm),
#        ]

    class band_summary(ReportBand):
        height = 0.7*cm
        elements = [
            Label(text="En total", top=0.1*cm, left=0),
            ObjectValue(attribute_name='id', top=0.1*cm, left=3*cm,
                action=FIELD_ACTION_COUNT,
                display_format='%s registros encontrados'),
        ]
        borders = {'all': True}

    class band_page_header(ReportBand):
        height = 1.3*cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1*cm,
                left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold',
                'fontSize': 14, 'alignment': TA_CENTER}),
            Label(text="Oficina", top=0.8*cm, left=0),
            Label(text="Nombre", top=0.8*cm, left=2*cm),
            Label(text="CI", top=0.8*cm, left=7*cm),
            Label(text="Empresa", top=0.8*cm, left=13*cm),
            Label(text="Fecha de Ingreso", top=0.8*cm, left=17*cm),
        ]
        borders = {'bottom': True}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='Reporte de la unidad', top=0.1*cm, left=0),
            SystemField(expression='Pagina # %(page_number)d de %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
        ]
        borders = {'top': True}

    class band_detail(ReportBand):
        height = 2.1*cm
        auto_expand_height = True
        margin_bottom = 0.4*cm
        elements = [
            ObjectValue(attribute_name='branchoffice.name', top=0, left=0),
            ObjectValue(attribute_name='guard.staff.full_name', top=0, left=2*cm, width=7*cm),
            ObjectValue(attribute_name='guard.staff.get_document', top=0, left=7*cm, width=7*cm),
            ObjectValue(attribute_name='guard.company.name', top=0, left=13*cm, width=7*cm),
            ObjectValue(attribute_name='get_date_joined_str', top=0, left=17*cm, width=7*cm),
        ]

class CarsReport(Report):
    title = 'Vehiculos'
#    page_size = letter
    page_size = landscape(letter)

#    class band_begin(ReportBand):
#        height = 1*cm
#        elements = [
#            Label(text='Registro de Vehiculos de un rango de fechas', top=0.1*cm,
#                left=8*cm),
#        ]

    class band_summary(ReportBand):
        height = 0.7*cm
        elements = [
            Label(text="En total", top=0.1*cm, left=0),
            ObjectValue(attribute_name='id', top=0.1*cm, left=3*cm,
                action=FIELD_ACTION_COUNT,
                display_format='%s registros encontrados'),
        ]
        borders = {'all': True}

    class band_page_header(ReportBand):
        height = 1.3*cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1*cm,
                left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold',
                'fontSize': 14, 'alignment': TA_CENTER}),
            Label(text="Interno", top=0.8*cm, left=0),
            Label(text="Placa", top=0.8*cm, left=1.5*cm),
            Label(text="Chasis", top=0.8*cm, left=4*cm),
            Label(text="Tipo", top=0.8*cm, left=9*cm),
            Label(text="Modelo", top=0.8*cm, left=15*cm),
            Label(text="Marca", top=0.8*cm, left=17*cm),
            Label(text="Kilometraje", top=0.8*cm, left=19*cm),
            Label(text="Parqueo", top=0.8*cm, left=21*cm),
        ]
        borders = {'bottom': True}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='Reporte de la unidad', top=0.1*cm, left=0),
            SystemField(expression='Pagina # %(page_number)d de %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
        ]
        borders = {'top': True}

    class band_detail(ReportBand):
        height = 0.5*cm
        elements = [
            ObjectValue(attribute_name='internal_number', top=0, left=0),
            ObjectValue(attribute_name='license_plate', top=0, left=1.5*cm, width=7*cm),
            ObjectValue(attribute_name='chassis', top=0, left=4*cm, width=7*cm),
            ObjectValue(attribute_name='type_motorized', top=0, left=9*cm, width=7*cm),
            ObjectValue(attribute_name='model_year', top=0, left=15*cm, width=7*cm),
            ObjectValue(attribute_name='manufacturer', top=0, left=17*cm, width=7*cm),
            ObjectValue(attribute_name='get_current_km', top=0, left=19*cm, width=7*cm),
            ObjectValue(attribute_name='branchoffice', top=0, left=21*cm, width=7*cm),
        ]

