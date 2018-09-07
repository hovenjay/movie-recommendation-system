# 基于 Python 的电影推荐系统

## 1. 项目简介

本项目是基于 Python Flask Web 框架开发的电影推荐系统。通过分析用户看过的电影和正在浏览的电影，推荐用户可能会感兴趣的内容。

### 1.1 相关技术

- 数据爬取：Python request、selenium；
- 数据库：MySQL；
- 后端：Flask 框架、Jinja2 模板引擎；
- 前端：HTML、CSS、JavaScript、jQuery、Ajax；

### 1.2 基本功能

- 用户登录：
  - 登陆功能；
  - 登陆持久化；
  - 注销登陆；
- 电影信息浏览：
  - 按分类查询电影；
  - 按评分升序或降序排列电影；
  - 浏览单部影片的详细信息；
- 个性化推荐算法
  - 相似推荐：根据用户正在浏览的电影，推荐相似的电影；
  - 猜你喜欢：根据用户的观影记录，推荐用户喜欢看的电影；
  - 喜欢这部电影的人也喜欢：根据当前用户的观影记录，推荐有着相似观影记录的用户看的最多的电影；

### 1.3 数据访问层

对于数据库的访问，由于做的是一个简单的推荐系统，大部分操作是查询数据库。数据访问层仅包含以下函数：

- douban_connect() ：数据库连接函数
- query() ：数据库查询函数
- get_user(username) ：查询单个用户的信息
- get_users() ：查询所有用户的信息
- user_login(username, password) ：校验用户名与密码是否匹配
- get_film(subject) ：获取单部电影的信息
- get_films(like, sort, page) ：获取某个分类下某一页的电影信息
- updata_film(con, subject, key, value) ：修改电影信息

### 1.4 业务逻辑层

- @app.route('/') ：主页面
- @app.route('/subject/\<int:sub\>/') ：影片详情页；
- @app.route('/show_uname',) ：API，根据浏览器 Session 和 Cookie 信息获取用户名；
- @app.route('/show_films') ：API，获取某分类一页影片的信息；
- @app.route('/show_recomm') ：API，获取推荐的电影；
- @app.route('/login') ：API，登陆校验；
- @app.route('/logout') ：注销登陆并清除 Cookie
- @app.errorhandler(404) ：404 页面

### 1.5 UI 表示层

UI 表示层是完全仿照豆瓣电影的风格制作的页面，主要有以下几个页面：

- 电影分类查询页：

  ![电影分类查询页](https://github.com/hovenjay/MovieRecommendationSystem/blob/master/static/img/page1.png)

- 影片详情页：

  ![影片详情页](https://github.com/hovenjay/MovieRecommendationSystem/blob/master/static/img/page2.png)

- 登陆注册页：

  ![登陆注册页](https://github.com/hovenjay/MovieRecommendationSystem/blob/master/static/img/page3.png)

- 豆瓣 404 页：

  ![豆瓣 404 页](https://github.com/hovenjay/MovieRecommendationSystem/blob/master/static/img/page4.png)

## 2. 效果展示

![演示图](https://github.com/hovenjay/MovieRecommendationSystem/blob/master/source/demonstration.gif)
