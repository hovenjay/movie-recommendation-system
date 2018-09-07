# 从本地 HTML 提取电影的 subject 和 title 属性，存储为 movielist.txt
# movielist.txt 读取电影的 subject 和 title 属性插入数据库 film_list 表
import re
import pymysql
from lxml import etree


def getMovieList(filename: str):
    # 解析本地 html 文件，获取编号和标题保存为 txt
    f = open(filename, 'r', encoding='utf-8')  # 打开文件
    html = f.read()  # 读取文件
    f.close()  # 关闭文件
    page = etree.HTML(html)  # 解析文档，找出标题和链接
    titles = page.xpath(
        '//*[@class="movie-list-panel pictext"]/div/div/div/div/span/a/text()')
    links = page.xpath(
        '//*[@class="movie-list-panel pictext"]/div/div/div/div/span/a/@href')
    f = open('movielist.txt', 'a', encoding='utf-8')  # 打开记录文件
    for (title, link) in zip(titles, links):
        subject = re.findall(r"[1-9][0-9]*", link)
        movie = str(subject[0]) + '\t' + title + '\n'
        f.write(movie)
    f.close()


def insertToDB(filename: str):
    # 解析格式化好的 txt 文本，并插入数据库
    f = open(filename, 'r', encoding='utf-8')  # 打开文件
    data = f.read()  # 读取文件
    f.close()  # 关闭文件
    ls1 = data.split('\n')
    ls2 = []
    for i in ls1:
        t = i.split('\t')
        if '' not in t:
            ls2.append(t)
    db = pymysql.connect("localhost", "root", "123456", "douban")
    cursor = db.cursor()
    for i in ls2:
        sql = "INSERT INTO film_list(subject,title) VALUES (" + i[0] + ",'" + i[1] + "')"
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception:  # 捕获所有异常
            db.rollback()
    db.close()


def main():
    for i in range(290):
        getMovieList('./html/' + str(i) + '.html')
    insertToDB('movielist.txt')


if __name__ == '__main__':
    main()
