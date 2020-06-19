function handleButtonClick() {

   var name = document.getElementById("name");
   var letters = /^[А-Яа-я]+$/;
    if(!letters.test(name.value)){
        alert('Проверьте ввод имени');
        document.callback.name.focus();
        return false;
    }

    var lastname = document.getElementById("lastname");
    if(!letters.test(lastname.value)){
        alert('Проверьте ввод фамилии');
        document.callback.name.focus();
        return false;
    }

    var phone = document.getElementById("phone");
    var login_len = phone.value.length;
    var letters = /^[8][0-9]{10}$/;
    if((!letters.test(phone.value))||(login_len != 11)){
        alert("Номер телефона должен состоять из 11 чисел");
        document.callback.name.focus();
        return false;
    }

    var town = document.getElementById("town");
    var letters = /^[А-Яа-я-]+$/;
    if(!letters.test(town.value)){
        alert('Проверьте ввод названия города');
        document.callback.name.focus();
        return false;
    }

    var email = document.getElementById("email");
    var letters = /^[a-z0-9_-]+@[a-z0-9]+\.[a-z]{2,6}$/i;
    if(!letters.test(email.value)){
        alert('Неправильно введен адрес электронной почты');
        document.callback.name.focus();
        return false;
    }

    var password = document.getElementById("password");
    var password_len = password.value.length;

    if (password_len < 8)
    {
        alert("Пароль должен содержать хотя бы 8 символов");
        document.callback.name.focus();
        return false;
    }
    else
    {
        if ((password.value.match(/[0-9]/)) && (password.value.match(/[A-ZА-Я]/)))
        {
            return true;
        }
        else
        {
            alert("Пароль должен содержать хотя бы 1 цифру и 1 Заглавную букву");
            document.callback.name.focus();
            return false;
        }
    }


}

// Получение переменной cookie по имени
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
console.log(csrftoken);

// Настройка AJAX
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        } else {
            alert('А вот и неправильно!'); // любое значение, кроме 2015
        }
    }
});


function like() {
    var like;
    like = $(this);
    var pk = like.data('id');
    console.log("Нажатие лайка")
    var action = like.data('action');
    var dislike = like.next();
    console.log(pk)
    $.ajax({
        url: "/inform/" + pk + "/" + action,
        type: 'POST',
        dataType: 'json',
        data: {'book': pk},
        success: function (json) {
            like.find("[data-count='like']").text(json.like_count);
            dislike.find("[data-count='dislike']").text(json.dislike_count);
        }
    });

    return false;
}

function dislike() {
    var dislike = $(this);
    var pk = dislike.data('id');
    console.log("Нажатие дизлайка")
    var action = dislike.data("action");
    var like = dislike.prev();
    console.log(pk)
    $.ajax({
        url: "/inform/" + pk + "/dislike",
        type: 'POST',
        data: {'book': pk},
        success: function (json) {
            dislike.find("[data-count='dislike']").text(json.dislike_count);
            like.find("[data-count='like']").text(json.like_count);
        }
    });
    return false;
}

// Подключение обработчиков
$(function () {
    document.querySelector("._LIKE_").addEventListener("click", like);

    document.querySelector("._DISLIKE_").addEventListener("click", dislike);
    // $('[data-action="like"]').click(like())
    //$('[data-action="dislike"]').click(dislike());
})