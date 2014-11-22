// using jQuery
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
var csrftoken = getCookie('csrftoken');

$(document).ready(function() {

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("#btn_login").click(function() {
        $.post("/api/account/login",
            {
                username: $("#txt_username").val(),
                password: $("#txt_password").val()
            },
            function(data) {
                window.location.href = ".";
            }
        ).fail(function(jqXHR, textStatus, errorThrown) {
            alert("Login failed, message: " + textStatus);
        });
    })

    $("#btn_logout").click(function() {
        $.get("/api/account/logout",
            function(data) {
                window.location.href = ".";
            }
        ).fail(function(jqXHR, textStatus, errorThrown) {
            alert("Logout failed, message: " + textStatus);
        });
    })
})
