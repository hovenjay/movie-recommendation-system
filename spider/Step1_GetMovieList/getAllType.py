# 获取所有的电影分类
import requests
from bs4 import BeautifulSoup


def write_to_file(fileName, s: str):
    f = open('./message/%s' % fileName, 'a', encoding='utf-8')
    f.write(s)
    f.close()


def main(url='https://movie.douban.com/chart'):
    typesHtml = requests.get(url)
    bs = BeautifulSoup(typesHtml.text, 'lxml')
    types = bs.find('div', class_='types').select('span')
    for t in types:
        typeName = t.a.get_text()
        typeHref = t.a.get('href')
        s = '%s\t%s\n' % (typeName, typeHref)
        print(s)


if __name__ == '__main__':
    main()