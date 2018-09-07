# 将 step2 获取的 17 个链接文件，分工给小组各成员，将每部电影页面保存至本地 html 文件
import os
import re
import time

import requests
from bs4 import BeautifulSoup


def write_to_file(fileName, s: str):
    f = open('./message/%s' % fileName, 'a', encoding='utf-8')
    f.write(s)
    f.close()


def get_movie_message(url):
    print(url)
    print()
    movieHtml = requests.get(url)
    fileName = re.findall('\d+', url)
    write_to_file('messageHtml/%s.html' % fileName[0], movieHtml.text)
    bs = BeautifulSoup(movieHtml.text, 'lxml')
    if bs.find('title').get_text() == '页面不存在':
        write_to_file('noFind.txt', url)
        return None
    movieName = bs.find(
        'span', attrs={
            'property': "v:itemreviewed"
        }).get_text()
    movieInfo = bs.find('div', class_='subject clearfix')
    movieImg = movieInfo.find('div', attrs={'id': "mainpic"}).img.get('src')
    info = movieInfo.find('div', attrs={'id': "info"}).text
    try:
        infoDict = re.search(r'导演:(?P<director> [\s\S]*?\n)', info).groupdict()
    except Exception:
        pass
    try:
        infoDict.update(
            re.search(r'编剧:(?P<writer>[\s\S]*?\n)', info).groupdict())
    except Exception:
        pass
    try:
        infoDict.update(
            re.search(r'主演:(?P<starring>[\s\S]*?\n)', info).groupdict())
    except Exception:
        pass
    try:
        infoDict.update(
            re.search(r'类型:(?P<classification>[\s\S]*?\n)', info).groupdict())
    except Exception:
        pass
    try:
        infoDict.update(
            re.search(r'制片国家/地区:(?P<country>[\s\S]*?\n)', info).groupdict())
    except Exception:
        pass
    try:
        infoDict.update(
            re.search(r'语言:(?P<language>[\s\S]*?\n)', info).groupdict())
    except Exception:
        pass
    try:
        infoDict.update(
            re.search(r'上映日期:(?P<release_date>[\s\S]*?\n)', info).groupdict())
    except Exception:
        pass
    try:
        infoDict.update(
            re.search(r'片长:(?P<film_length>[\s\S]*?\n)', info).groupdict())
    except Exception:
        pass
    try:
        infoDict.update(
            re.search(r'又名:(?P<alias>[\s\S]*?\n)', info).groupdict())
    except Exception:
        pass
    try:
        infoDict.update(
            re.search(r'IMDb链接:(?P<IMDB>[\s\S]*?\n)', info).groupdict())
    except Exception:
        pass
    movieScore = bs.find('strong', class_='ll rating_num').get_text()
    movieVister = bs.find('span', attrs={'property': 'v:votes'}).get_text()
    movieRatio = bs.find('div', class_='rating_betterthan').get_text()
    if bs.find('span', class_='all hidden') != None:
        movieIntroduction = bs.find('span', class_='all hidden').get_text()
    elif bs.find('div', attrs={'id': "link-report"}) != None:
        movieIntroduction = bs.find(
            'span', attrs={
                'property': "v:summary"
            }).get_text()
    else:
        movieIntroduction = ''
    movieCommonLabel = [
        a.get_text() for a in bs.find('div', class_='tags-body').select('a')
    ]
    movieSeenQuantity = bs.find(
        'div', class_='subject-others-interests-ft').select('a')[0].get_text()
    movieWantToSee = bs.find(
        'div', class_='subject-others-interests-ft').select('a')[1].get_text()
    infoDict.update({'title': '%s' % movieName})
    infoDict.update({'imgSrc': '%s' % movieImg})
    infoDict.update({'score': '%s' % movieScore})
    infoDict.update({'vister': '%s' % movieVister})
    infoDict.update({'ratio': '%s' % movieRatio})
    infoDict.update({
        'introduction': '%s' % re.sub(' ', '', movieIntroduction)
    })
    infoDict.update({'common_label': '%s' % movieCommonLabel})
    infoDict.update({'seen_quantity': '%s' % movieSeenQuantity})
    infoDict.update({'want_to_see': '%s' % movieWantToSee})
    print(infoDict, end='\n\n')
    write_to_file('getLog/log.txt', str(url) + '\n')
    # 存储字典包含：导演、编剧、主演、类型、国家、语言、日期、片长、又名、IMDb、
    # 片名、图片连接、评分、评分人数、分类排行百分比、简介、常用标签、看过人数、想看人数
    write_to_file('info.txt', str(infoDict) + '\n')


def get_all():
    FileName = '0.txt'
    urlFile = open('./message/%s' % FileName, 'r', encoding='utf-8')
    urlList = urlFile.read().split('\n')
    urlFile.close()
    if urlList[0] == '':
        return None
    url = 'https://movie.douban.com/subject/%s/' % urlList.pop(0)
    get_movie_message(url)
    os.remove('./message/%s' % FileName)
    for u in urlList:
        write_to_file(FileName, u + '\n')
    time.sleep(0)
    get_all()


if __name__ == '__main__':
    get_all()
