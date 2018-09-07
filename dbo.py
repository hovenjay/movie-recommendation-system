import pymysql


def douban_connect():  # 连接数据库
    # 返回数据库连接的对象 con，调用需要手动关闭连接
    con = pymysql.Connect(
        # host='192.168.14.129',
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='douban',
        charset='utf8')
    return con


def query(sql: str):  # 执行任何 sql 查询
    con = douban_connect()
    cursor = con.cursor()
    try:
        cursor.execute(sql)
        con.commit()
    except Exception:
        con.rollback()
        print("发生异常", Exception)
        print(sql)
    con.close()


def get_user(username: str) -> dict:  # 获取单个用户信息
    # 参数为用户名，返回包含用户信息的字典
    # 字典第一个元素 row 为 0 表示未查询到用户
    # 字典第一个元素 row 为 1 表示查询到用户
    # 返回示例：{'row': 1, 'uname': 'admin', 'email': 'admin@db.com', 'passwd': '123456'}
    user = {'row': 0, 'uname': '', 'email': '', 'passwd': '', 'viewed': ''}
    con = douban_connect()
    cursor = con.cursor()
    sql = "SELECT * FROM `user_list` WHERE BINARY `uname` = '%s';" % (username)
    cursor.execute(sql)
    row = cursor.rowcount  # 获取的行数
    if row == 1:
        result = cursor.fetchone()  # 返回元组
        user['row'] = row
        user['uname'] = result[0]
        user['email'] = result[1]
        user['passwd'] = result[2]
        user['viewed'] = result[3]
    con.close()
    return user


def get_users() -> tuple:  # 获取用户列表
    # 无参，返回包含所有用户信息的集合 ()
    # 返回值示例：(('admin', 'admin@db.com', '123456'),)
    con = douban_connect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM `user_list`")
    users = cursor.fetchall()
    con.close()
    return users


def user_login(username: str, password: str) -> dict:  # 登陆校验函数
    # 参数为用户名，返回包含登陆结果信息的字典
    # 登陆成功：result = True，info = '登陆成功'
    # 登陆失败：result = False，info = '用户不存在' / '密码不正确'
    msg = {'result': False, 'info': ''}
    user = get_user(username)
    if user['row'] == 1:
        if user['passwd'] == password:
            msg = {'result': True, 'info': '登陆成功'}
        else:
            msg = {'result': False, 'info': '密码不正确'}
    else:
        msg = {'result': False, 'info': '用户不存在'}
    return msg


def get_film(subject: int) -> tuple:  # 获取单部电影的信息
    # 参数为 subject，返回包含单部电影信息的元组
    # 查询到则返回电影信息，未查询到返回空元组
    con = douban_connect()
    cursor = con.cursor()
    sql = "SELECT * FROM `film_list` WHERE `subject` = %s" % (subject)
    cursor.execute(sql)
    result = cursor.fetchone()  # 返回元组
    con.close()
    return result


def get_all_films(like: str) -> tuple:  # 按分类获取分类下全部电影列表信息
    if like == '':  # 如果筛选值为空，则匹配全部
        like = '%'
    else:
        like = '%' + like + '%'
    con = douban_connect()
    cursor = con.cursor()
    sql = "SELECT * FROM `film_list` WHERE `classification` LIKE '%s';" % (
        like)
    cursor.execute(sql)
    result = cursor.fetchall()
    con.close()
    return result


def get_films(like: str, sort: str, page: int) -> tuple:  # 按分类分页获取电影列表信息
    # 参数为：筛选值，排序规则(ASC:升序，DESC:降序)，页号
    # 返回包含一组电影信息的元祖
    if like == '':  # 如果筛选值为空，则匹配全部
        like = '%'
    else:
        like = '%' + like + '%'
    if sort != 'ASC' and sort != 'DESC':  # 默认降序
        sort = 'DESC'
    if page < 0:  # 如果页号小于 0，从第 0 条开始读取
        page = 0
    else:
        page = page * 30
    con = douban_connect()
    cursor = con.cursor()
    sql = "SELECT * FROM `film_list` WHERE `classification` LIKE '%s' ORDER BY `score` %s LIMIT %s,30;" % (
        like, sort, page)
    cursor.execute(sql)
    result = cursor.fetchall()
    con.close()
    return result


def updata_film(con, subject, key, value):  # 插入电影详细信息到数据库
    # 参数为：数据库连接对象，subject，字段，字段的值
    # 插入正常输出受影响的行数
    # 插入异常情况输出 sql 语句
    cursor = con.cursor()
    sql = "UPDATE `film_list` SET `" + str(key) + "` = '" + str(
        value) + "' WHERE `film_list`.`subject` = " + str(subject) + ";"
    try:
        cursor.execute(sql)
        con.commit()
        print("cursor.excute:", cursor.rowcount)
    except Exception:
        con.rollback()
        print("发生异常", Exception)
        print(sql)


# 调用测试
# print(get_user('july'))
# print(get_users())
# print(user_login('july', '123'))
# print(get_film(1293116))
# like = '科幻'
# sort = ''
# page = 0
# result = get_films(like, sort, page)
# for i in result:
#     print("%s \t %s " % (i[0], i[1]))
