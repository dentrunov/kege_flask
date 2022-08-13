var slide_num = 1

function show_task(num) {
    var slides = document.getElementsByClassName('slide');
    var liti = document.getElementsByClassName('liti');

    if (num > slides.length) {
        num = 0;
    }
    if (num < 1) {
        num = slides.length;
    }
    if (num == 1) {
        $('#prevbutton').css("display", "none");
    } else {
        $('#prevbutton').css("display", "block");
    }
    if (num == slides.length) {
        $('#nextbutton').css("display", "none");
    } else {
        $('#nextbutton').css("display", "block");
    }

    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
        liti[i].style.background = "antiquewhite";
        liti[i].style.color = "#000";

    }
    slides[num - 1].style.display = "block";
    liti[num - 1].style.background = "navy";
    liti[num - 1].style.color = "#FFF";

}

function butcklick(num) {
    slide_num = num + 1
    show_task(slide_num);
}

function next() {
    slide_num += 1
    show_task(slide_num);
}

function previous() {
    slide_num -= 1
    show_task(slide_num);
}

function choose_task(num) {
    show_task(slide_num = num)
}
$(document).ready(function() {
     tp = $("#tasks").scrollTop();
    $("#tasks").on("scroll", function () {
        var tp = $("#tasks").scrollTop();
        if (tp > 30) {
            $('#litiup').css("background-color", "navy");
        } else {
            $('#litiup').css("background-color", "aliceblue");
        }
        if (tp < 300) {
            $('#litidn').css("background-color", "navy");
        } else {
            $('#litidn').css("background-color", "aliceblue");
        }
    });


$('#litiup').on("click", function() {
    var tp = $("#tasks").scrollTop();
    $("#tasks").scrollTop(tp - 20);
});
$('#litidn').on("click", function() {
    var tp = $("#tasks").scrollTop();
    $("#tasks").scrollTop(tp + 20);
});

});


$(document).ready(function() {
    //функция обработки и сохранения вопроса
    $(".fm").submit(function(event) {
        event.preventDefault();
        var form_id = $(this).closest("form").attr('id');

        $.ajax({
            url: "/taskcheck",
            type: "POST",
            data: $('#' + form_id).serialize(),
            success: function(result) {
                $("#message").slideToggle(1000);
                $("#message").html('Сохранено');
                $("#message").slideToggle(1000);
            }
        });
        event.stopImmediatePropagation();
    });


    //функция сохранения формы
    $(".usr").submit(function(event) {
        event.preventDefault();
        var form_id = $(this).closest("form").attr('id');
        var user = form_id.split('_').slice(-1);

        $.ajax({
            url: "/changegroup",
            type: "POST",
            data: $('#' + form_id).serialize(),
            success: function(result) {
                $("#message").slideToggle(1000);
                $("#message").html('Сохранено');
                $("#message").slideToggle(1000);
                $("#user_tr_"+user).css("display", "none");
            }
        });
        event.stopImmediatePropagation();
    });

    $(".delete_link").on('click',function (event) {
    event.preventDefault();
    var t_id = $(this).parent().siblings('.change_id').text();
    var del_ = confirm('Вы хотите удалить тест?');
         if (del_) {
              $.ajax({
                    url: "/adminpage_delete_test",
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify({'t_id': t_id}),
                        success: function(result) {
                            $("#tr_"+t_id).css('display','none');
                         }
                    });
         };
        event.stopImmediatePropagation();
    });

    $(".change_link").on('click',function (event) {
    event.preventDefault();
    var t_id = $(this).parent().siblings('.change_id').text();
    if ($(this).text() == 'Показать') {
        var txt = 'Скрыть';
    }
    else {
        var txt = 'Показать'
    };
    var del_ = confirm('Вы хотите изменить видимость теста?');
         if (del_) {
              $.ajax({
                    url: "/adminpage_hide_test",
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify({'t_id': t_id}),
                        success: function(result) {
                            $("#a_"+t_id).text(txt);
                         }
                    });
         };
        event.stopImmediatePropagation();
    });


//функция показа/сокрытия родителя для ученика в форме настройки пользователя
    $("#role").change(function (event) {
        event.preventDefault();
        var role = $("#role").val()
        if (role == 3) {
            $("#parent_email").css('display','block');
        }
        else {
            $("#parent_email").css('display','none');
        };
    });
});





    //функция завершения теста
 function finish_test() {
     event.preventDefault()
         var end = confirm('Вы хотите завершить тест?')
         if (end) {
              $.ajax({
            url: "/finishtest",
            success: function(result) {
                location.href = '../showresult/'+$.parseJSON(result).msg;
            }
        });
         };
        event.stopImmediatePropagation();
     };

    function startTimer() {
        var my_timer = document.getElementById("my_timer");
        var time = my_timer.innerHTML;
        var arr = time.split(":");
        var h = arr[0];
        var m = arr[1];
        var s = arr[2];
        if (s == 0) {
        if (m == 0) {
        if (h == 0) {
            alert("Ваше время вышло");
            //window.location.reload();
            finish_test()
            return;
        }
        h--;
        m = 60;
        if (h < 10) h = "0" + h;
        }
        m--;
        if (m < 10) m = "0" + m;
        s = 59;
        }
        else s--;
        if (s < 10) s = "0" + s;
        document.getElementById("my_timer").innerHTML = h+":"+m+":"+s;
        setTimeout(startTimer, 1000);
    }
