var like = '' // 分类
var sort = '' // 升序/降序
var page = 0 // 页号
var flags = false; // 滚动监视标志

$(window).on("load", function () { // 当窗口加载完毕，加载一页内容，加载当前登陆用户，加载推荐的影片
    $.post("/show_uname", {},
        function (results, status) {
            var msg = jQuery.parseJSON(results);
            if (msg.result) {
                logged(msg.info);
            } else {
                login();
            }
        });
    request_page(); // 请求第一页数据
});

$(window).scroll(function () { // 当滚动至距离页脚一定距离，继续加载内容
    var minAwayBottom = 150; // 距离页面底部的最小距离
    var awayBottom = $(document).height() - $(window).scrollTop() - $(window).height();
    // console.log('当前距离页面底部：' + awayBottom + 'px');
    if (awayBottom <= minAwayBottom) {
        if (flags) {
            page = page + 1;
            request_page();
        }
    }
});

$(window).scroll(function () { // 当滚动一定距离，推荐窗口浮动
    var winPos = $(window).scrollTop(); // 当前滚动位置距离页面顶部的距离
    var div_top = $("#doubanapp6").offset().top; // div 距离页面顶部的距离
    if (winPos > div_top) {
        $("#recomandDiv").attr("class", "fixed-top");
    } else {
        $("#recomandDiv").attr("class", "fixed");
    }
});

$(document).ready(function () { // 切换分类
    $(".tag").click(function () {
        $('ul.category li').children().attr("class", "tag");
        $(this).attr("class", "tag-checked tag");
        like = $(this).text();
        if (like == '全部类型') {
            console.log(like)
            like = ''
            console.log(like)
        }
        page = 0;
        flags = true;
        $("#films").html("");
        request_page();
    });
});

$(document).ready(function () { // 切换排序
    $(".tabs a").click(function () {
        $(this).siblings().attr("class", "tab");
        $(this).attr("class", "tab-checked");
        sort = $(this).attr("value");
        page = 0;
        flags = true;
        $("#films").html("");
        request_page();
    });
});

function request_page() { // 请求一页数据和该页的推荐内容
    flags = false; // 加锁
    $.post("/show_films", {
            'like': like,
            'sort': sort,
            'page': parseInt(page),
        },
        function (results, status) {
            var filmlist = jQuery.parseJSON(results);
            console.log(filmlist);
            if (filmlist.length > 0) {
                createFilms("films", filmlist);
            }
        });
    $.post("/show_recomm", {
            'like': like,
            'sort': sort,
            'page': parseInt(page),
        },
        function (results, status) {
            var filmlist = jQuery.parseJSON(results);
            if (filmlist.length > 0) {
                document.getElementById('recommandfilms').innerHTML = "";
                createFilms("recommandfilms", filmlist);
                flags = true; // 解锁
            }
        });
}

function createFilms(elementid, filmlist) { // 创建一页电影的信息块
    var parent = document.getElementById(elementid); // 根节点对象
    for (i = 0; i < filmlist.length; i++) {
        var subject = filmlist[i][0];
        var title = filmlist[i][1];
        var score = filmlist[i][9];
        var imgsrc = filmlist[i][21];
        var title1 = title.split(" ");
        var title2 = title1[0];
        // console.log(subject);
        var son = document.createElement('a'); // 根节点下创建一部电影
        son.setAttribute("target", "_Blank"); // 设置一部电影的基本属性
        son.setAttribute("href", "/subject/" + String(subject) + "/");
        son.setAttribute("class", "item")
        son.setAttribute("id", String(subject));
        parent.appendChild(son); // 将电影添加进电影列表
        var movie = document.getElementById(String(subject)); // 找到该电影，为电影添加其它信息
        movie.innerHTML = "<div class='cover-wp'> <span class='pic'> <img src='" + imgsrc + "'></span></div><p><span class='title'>" + title2 + " </span><span  class='rate'>" + score + "</span></p>";
    }
}

function login() { // 未登录状态显示
    var login_1 = document.getElementById('login_status1');
    var login_2 = document.getElementById('login_status2');
    login_1.setAttribute("href", "/login");
    login_1.innerText = "登录";
    login_2.setAttribute("href", "/register");
    login_2.innerText = "注册";
}

function logged(username) { // 登陆状态显示
    var login_1 = document.getElementById('login_status1');
    var login_2 = document.getElementById('login_status2');
    login_1.setAttribute("href", "#");
    login_1.innerText = username;
    login_2.setAttribute("href", "/logout");
    login_2.innerText = "注销";
}