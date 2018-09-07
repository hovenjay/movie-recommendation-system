# 从每个分类的每个评分段的页面保存为 html 文件，存放在 ./html
import time
from selenium import webdriver


def Categorys(category: [], links):  # 生成要爬取的链接列表
    for ca in category:
        a = 100
        b = 90
        while b >= 0:
            links.append(ca + str(a) + ':' + str(b) + '&action=')
            a = a - 10
            b = b - 10


def scroll(driver):  # 页面滚动函数
    driver.execute_script("""
        (function () {
            var y = document.body.scrollTop;
            var step = 100;
            window.scroll(0, y);
            function f() {
                if (y < document.body.scrollHeight) {
                    y += step;
                    window.scroll(0, y);
                    setTimeout(f, 200);
                }
                else {
                    window.scroll(0, y);
                    document.title += "scroll-done";
                }
            }
            setTimeout(f, 2000);
        })();
        """)


def getMovieList(driver, index, link):  # 爬取某个分类函数
    driver.get(link)
    scroll(driver)
    time.sleep(30)
    f = open('./html/' + str(index) + '.html', 'w', encoding='utf-8')
    f.write(driver.page_source)
    f.close()


def main():
    # 初始化浏览器驱动
    chromedriver = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver)
    # 主程序
    category = []  # 创建五个分类的基本链接
    category.append(
        'https://movie.douban.com/typerank?type_name=剧情&type=11&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=喜剧&type=24&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=动作&type=5&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=爱情&type=13&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=科幻&type=17&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=动画&type=25&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=悬疑&type=10&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=惊悚&type=19&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=恐怖&type=20&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=纪录片&type=1&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=短片&type=23&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=情色&type=6&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=同性&type=26&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=音乐&type=14&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=歌舞&type=7&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=家庭&type=28&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=儿童&type=8&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=传记&type=2&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=历史&type=4&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=战争&type=22&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=犯罪&type=3&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=西部&type=27&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=奇幻&type=16&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=冒险&type=15&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=灾难&type=12&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=武侠&type=29&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=古装&type=30&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=运动&type=18&interval_id=')
    category.append(
        'https://movie.douban.com/typerank?type_name=黑色电影&type=31&interval_id='
    )
    links = []  # 创建链接表
    Categorys(category, links)  # 调用函数为每个分类生成十条链接
    for index, link in enumerate(links):
        print(str(index) + ":" + link)
        getMovieList(driver, index, link)
    driver.close()
    driver.quit()


if __name__ == '__main__':
    main()
