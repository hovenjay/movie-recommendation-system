$(window).on("load", function () { // 当窗口加载完毕，加载一页内容
    $.post("/show_uname", {},
        function (results, status) {
            var msg = jQuery.parseJSON(results);
            console.log(msg.result)
            if (msg.result) {
                logged(msg.info);
            } else {
                login();
            }
        });
})

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
