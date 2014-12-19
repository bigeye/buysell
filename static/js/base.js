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
        username = $("#txt_username").val();
        password = $("#txt_password").val();

        if (username == "") {
            alert("Please Input User ID");
            $("#txt_username").focus();
        }
        else if (password == "") {
            alert("Please Input Password");
            $("#txt_password").focus();
        }
        else {
            $.post("/api/account/login",
                {
                    username: username,
                    password: password
                },
                function(data) {
                    window.location.href = ".";
                }
            ).fail(function(jqXHR, textStatus, errorThrown) {
                alert("Login failed. / message: " + textStatus);
            });
        }
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

    $("#btn_to_register").click(function() {
        window.location.href = "/register";
    });

    $("#btn_register").click(function() {
        var password1, password2;
        password = $("#txt_password").val();
        password_confirm = $("#txt_password_confirm").val();

        alert(password);
        alert(password_confirm)

        if (password == password_confirm) {
            $.post("/api/account/register",
                {
                    username: $("#txt_username").val(),
                    email: $("#txt_email").val(),
                    password: password1
                },
                function(data) {
                    alert('Registration successful.');
                    window.location.href = "/";
                }
            ).fail(function(jqXHR, textStatus, errorThrown) {
                alert("Registration failed. / message: " + textStatus);
            });
        }
        else {
            alert("Passwords do not match, please check again!");
        }
    });
})
