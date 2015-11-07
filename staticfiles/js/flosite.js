
/*
###############################################################################
################## Seccion importante para el manejo de AJAX ##################
###############################################################################
*/

$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

/*
############################# FIN DE AJAX ####################################
###############################################################################
*/

/*
function validation_car(){
    internal_number_automotive = $('input#id_car').val()
    $.ajax({
        type: "POST",
        url : "/register/ajax_validation_car/",
        data: {
            'car': internal_number_automotive
        },
        dataType: 'json',
        success: function(response){
            $('input#id_employee').val($.parseJSON(response.driver))
            $('input#id_km').val($.parseJSON(response.km))
            $('input#id_ladders').val($.parseJSON(response.dev))
        },
        error: function(){
            alert('El interno del Vehiculo es incorrecto')
        }
    });
}
*/

function searchGuest(){
    $.ajax({
        type: "POST",
        url : "/guest/search/",
        data: {
            'val_document': $('input#id_val_document').val()
        },
        success: function(response){
            $('div#complete_info_guest').html(response)
        },
        error: function(){
            alert('Ocurrio un error')
        }
    });
}

function viewNotification(id_notification){
    $.ajax({
        type: "POST",
        url : "/notifications/"+ id_notification +"/view/",
        success: function(response){
            $('div#view_notification').html(response)
        },
        error: function(){
            alert('Erro al cargar la notificacion')
        }
    });
}
function maintenance_car(){
    $.ajax({
        type: "POST",
        url : "/maintenance/program/ajax_sidebar/",
        data: {
            'internal_number': $('input#id_internal_number').val()
        },
        success: function(response){
            $('div#sidebar').html(response)
        },
        error: function(){
            alert('El interno del Vehiculo es incorrecto')
        }
    });
}

function validation_car(){
    $.get('/register/ajax_validation_car/', {car: $('input#id_car').val()}).done(function(data){
        $.each(data, function(key, value) {
            if (key == "km") {
                $('input#id_km').val(value)
            }
            if (key == "driver") {
                $('input#id_employee').val(value)
            }
            if (key == "ladders") {
                $('input#id_ladders').val(value)
            }
            if (key == "in_moving") {
                if (value){
                    document.getElementById('id_km').readOnly=false
                } else {
                    document.getElementById('id_km').readOnly=true
                }
            }
        });
    })
    .fail(function() {
        alert('El numero de interno del Vehiculo es incorrecto')
    });
    if ($('div#sidebar')[0] != null) {
        $.ajax({
            type: "POST",
            url : "/register/ajax_sidebar/",
            data: {
                'car': $('input#id_car').val()
            },
            success: function(response){
                $('div#sidebar').html(response)
                if ($('input#event_car').val() == "salida") {
                    $('div#div_maintenance').html('<div class="alert fade in  alert-info">' +
                                                  '  <input type="checkbox" id="maintenance" name="maintenance">' +
                                                  '    <b>Taller:</b> El vehiculo ingreso a taller para mantenimiento' +
                                                  '  </input>' +
                                                  '</div>')
                    $('div#div_message').html('')
                    $('div#div_km_revert').html('')
                } else {
                    if ($('input#event_car').val() == "retorno") {
                        $('div#div_maintenance').html('')
                        $('div#div_km_revert').html('<div class="alert fade in  alert-info">' +
                                                    '  <input type="checkbox" id="km_revert" name="km_revert">' +
                                                    '   <b>Giro de reloj</b>' +
                                                    '  </input>' +
                                                    '</div>')
                        $('div#div_message').html('')
                        if ($('input#workshop').val() == 'workshop') {
                            $('div#div_message').html('<div class="alert fade in  alert-danger">' + 
                                                      '  <a data-dismiss="alert" href="#" class="close">×</a>' +
                                                      '    <h4>El Vehiculo esta en taller, ' +
                                                      '    si continua quiere decir que el ' + 
                                                      '    Vehiculo esta de retorno</h4>' + 
                                                      '</div>')
                        } else {
                            $('div#div_message').html('')
                        }
                    } else {
                        $('div#div_message').html('')
                        $('div#div_maintenance').html('<div class="alert fade in  alert-info">' +
                                                      '    <input type="checkbox" id="maintenance" name="maintenance">' +
                                                      '        <b>Taller:</b> El vehiculo ingreso a taller para mantenimiento' +
                                                      '    </input>' +
                                                      '</div>')

                    }

                }
            },
            error: function(){
                alert('El interno del Vehiculo es incorrecto')
            }
        });
    }
}

function getTime(){
    var currentTime = new Date()
    var hours = currentTime.getHours()
    var minutes = currentTime.getMinutes()
    if (minutes < 10){
        minutes = "0" + minutes
    }
    return hours + ":" + minutes
}

function delete_date_session(){
    $.ajax({
        type: "POST",
        url : "/register/ajax_delete_date_session/"
//        success: function(data){
//            $('div#message_date').html(data)
//        }
    });
}

function stopTimePerson(id){
    $.get("/register/guest/" + id + "/stop/").done(function(data){
            $('div#stop_person_' + id).html(data)
    });
    if (document.getElementById("tr_person_" + id).className == "danger") {
        document.getElementById("tr_person_" + id).className = "active"
    }
}

function validation_km(){
    a = parseInt($('span#last_km').html())
    b = parseInt($('input#id_km').val())
    diff_km = b - a
    is_revert = $("input#km_revert").is(":checked")
    if ( a > b ) {
        if ( !is_revert ){
            alert('El kilometraje ingresado es incorrecto')
        }
    } else {
        mm = validation_tm_km()
        if (mm <= 60 & diff_km > 80) {
            alert('ERROR: En ' + mm + ' minutos no pudo haber recorrio ' + diff_km +' Km')
        } else {
            if (mm <= 120 & diff_km > 200) {
                alert('ERROR: En menos de 2 horas no pudo haber recorrio ' + diff_km + ' Km')
            } else {
                if (mm <= 1400 & diff_km >= 1000) {
                    alert('ERROR: No es posible que en ' + Math.floor(mm/60) + ' horas haya recorrido ' + diff_km + ' Km')
                }
            }
        }
    }
}

function validation_tm_km(){
    if ($('input#rdate').length > 0) {
        dlast = $('input#rdate').val().split('-')
        dtime = $('input#rtime').val().split(':')
        datelast = new Date(dlast[0], dlast[1] - 1, dlast[2], dtime[0], dtime[1])

        if ($('input#rdatecurrent').length > 0) {
            dcurrent = $('input#rdatecurrent').val().split('-')
            tcurrent = $('input#id_time').val().split(':')
            datecurrent = new Date(dcurrent[0], dcurrent[1] - 1, dcurrent[2], tcurrent[0], tcurrent[1])
        } else {
            dcurrent = $('input#id_register_date').val().split('-')
            tcurrent = $('input#id_time').val().split(':')
            datecurrent = new Date(dcurrent[0], dcurrent[1] - 1, dcurrent[2], tcurrent[0], tcurrent[1])

        }
        var diff = datecurrent - datelast
        var msec = diff

        var hh = Math.floor(msec / 1000 / 60 / 60);
        msec -= hh * 1000 * 60 * 60;
        var mm = Math.floor(msec / 1000 / 60);
        if (hh == 1) {
            return 60 + mm
        } else {
            if (hh > 1) {
                return (hh*60) + mm
            } else {
                return mm
            }
        }
    }
}

function validation_time() {
    if ($('input#id_time').val().split(':').length != 2) {
        alert('ERROR: La hora es incorrecto, debe colocar de la siguiente forma HH:MM')
    }
}
