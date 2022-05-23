function clss() {
    $('#splash').css("display", "none");
}

var slide_num = 1

function show_task(num) {
    var slides = document.getElementsByClassName('slide');
    var liti = document.getElementsByClassName('liti');
    var fm = document.getElementsByClassName('fm');

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
        fm[i].style.display = "none";
        liti[i].style.background = "antiquewhite";
        liti[i].style.color = "#000";

    }
    slides[num - 1].style.display = "block";
    if (num - 1 != 0) fm[num - 1].style.display = "block";
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

var top = $("#tasks").scrollTop();
$("#tasks").on("scroll", function() {
    var top = $("#tasks").scrollTop();
    if (top > 30) {
        $('#litiup').css("background-color", "navy");
    } else {
        $('#litiup').css("background-color", "aliceblue");
    }
    if (top < 300) {
        $('#litidn').css("background-color", "navy");
    } else {
        $('#litidn').css("background-color", "aliceblue");
    }
});
$('#litiup').on("click", function() {
    var top = $("#tasks").scrollTop();
    $("#tasks").scrollTop(top - 20);
});
$('#litidn').on("click", function() {
    var top = $("#tasks").scrollTop();
    $("#tasks").scrollTop(top + 20);
});

$(document).ready(function() {
    $(".sub").click(function(event) {
        event.preventDefault();
        let form_id = $(this).closest("form").attr('id');

        $.ajax({
            url: "admin/taskcheck.php",
            type: "POST",
            data: $('#' + form_id).serialize(),
            success: function(result) {
                $("#addover").slideToggle(1000);
                $("#addover").html(result);
                $("#addover").slideToggle(1000);

            }
        });
        event.stopImmediatePropagation();
    });
});

$(document).ready(function() {
    $("#endtest").click(function(event) {
        event.preventDefault();
        $("#addover").slideToggle(1000);
        $("#addover").html('<p>Р—Р°РІРµСЂС€РёС‚СЊ С‚РµСЃС‚РёСЂРѕРІР°РЅРёРµ?</p><p><a href="test.php?act=endtest">РџРѕРґС‚РІРµСЂРґРёС‚СЊ</a></p>');

    });
});

function finish_test() {
    $("#addover").slideToggle(1000);
    $("#addover").html('<p>Завершить тестирование?</p><p><a href="test.php?act=endtest">Подтвердить</a></p>');

}
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
