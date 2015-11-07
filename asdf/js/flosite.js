
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
        });
    })
    .fail(function() {
        alert('El numero de interno del Vehiculo es incorrecto')
    });
}

