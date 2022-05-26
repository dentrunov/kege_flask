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

var top = $("#tasks").scrollTop();
$("#tasks").on("scroll", function() {
    var top = $("#tasks").scrollTop();
    Console.log(top);
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
