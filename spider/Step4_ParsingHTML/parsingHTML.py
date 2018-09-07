import re
import os
import json
from bs4 import BeautifulSoup


# 获取html页面
def openFile(fileName):
    files = open('../messageHtml/%s' % fileName, 'r', encoding='utf-8')
    filestring = files.read()
    files.close()
    return filestring


# 对html页面进行解析
def getHtmlMessage(url):
    print(url, end='\n\n')
    fString = openFile(url + '.html')
    bs = BeautifulSoup(fString, 'lxml')
    if bs.find('title').get_text() == '页面不存在':
        if not os.path.isdir('../log'):
            os.makedirs('../log')
        with open('../log/logCantFind.txt', 'a', encoding='utf-8') as fileNotFind:
            fileNotFind.write(url + '\n')
        return None
    infoDict = {}
    infoDict['subject'] = int(url)
    infoDict['title'] = bs.find(
        'span', attrs={'property': "v:itemreviewed"}).get_text()
    movieInfo = bs.find('div', class_='subject clearfix')
    info = movieInfo.find('div', attrs={'id': "info"}).text
    try:
        movieImg = movieInfo.find(
            'div', attrs={'id': "mainpic"}).img.get('src')
        if not os.path.isdir('../img'):
            os.makedirs('../img')
        with open('../img/imgSrc.txt', 'a', encoding='utf-8') as fileImg:
            fileImg.write('%s\t%s\n' % (url, movieImg))
        infoDict['strb'] = movieImg
    except Exception:
        infoDict['strb'] = ''
    try:
        alias = re.search(r'又名:(?P<alias>[\s\S]*?)\n', info).groupdict()
        infoDict['alias'] = '%s' % (re.sub(
            '[ ]/[ ]', '\t', alias['alias'])).strip()
    except Exception:
        infoDict['alias'] = ''
    try:
        director = re.search(r'导演:(?P<director> [\s\S]*?)\n', info).groupdict()
        infoDict['director'] = '%s' % (re.sub(
            '[ ]/[ ]', '\t', director['director'])).strip()
    except Exception:
        infoDict['director'] = ''
    try:
        writer = re.search(r'编剧:(?P<writer>[\s\S]*?)\n', info).groupdict()

        infoDict['writer'] = '%s' % (re.sub(
            '[ ]/[ ]', '\t', writer['writer'])).strip()
    except Exception:
        infoDict['writer'] = ''
    try:
        starring = re.search(r'主演:(?P<starring>[\s\S]*?)\n', info).groupdict()
        infoDict['starring'] = '%s' % (re.sub(
            '[ ]/[ ]', '\t', starring['starring'])).strip()
    except Exception:
        infoDict['starring'] = ''
    try:
        classification = re.search(
            r'类型:(?P<classification>[\s\S]*?)\n', info).groupdict()

        infoDict['classification'] = '%s' % (re.sub(
            '[ ]/[ ]', '\t', classification['classification'])).strip()
    except Exception:
        infoDict['classification'] = ''
    try:
        country = re.search(
            r'制片国家/地区:(?P<country>[\s\S]*?)\n', info).groupdict()
        infoDict['country'] = '%s' % (re.sub(
            '[ ]/[ ]', '\t', country['country'])).strip()
    except Exception:
        infoDict['country'] = ''
    try:
        language = re.search(r'语言:(?P<language>[\s\S]*?)\n', info).groupdict()

        infoDict['language'] = '%s' % (re.sub(
            '[ ]/[ ]', '\t', language['language'])).strip()
    except Exception:
        infoDict['language'] = ''
    try:
        infoDict['score'] = float(
            bs.find('strong', class_='ll rating_num').get_text())
        retio = bs.find(
            'div', class_='rating_betterthan').get_text().strip()
        infoDict['ratio'] = '%s' % (re.sub(
            '[ ]*\n[ ]*', '\t', retio))
    except Exception:
        infoDict['score'] = 0
        infoDict['ratio'] = ''
    try:
        movieVister = bs.find('span', attrs={'property': 'v:votes'}).get_text()
        infoDict['num2'] = int(movieVister)
    except Exception:
        infoDict['num2'] = 0
    try:
        release_date = re.search(
            r'上映日期:(?P<release_date>[\s\S]*?)\n', info).groupdict()
        infoDict['release_date'] = '%s' % (re.sub(
            '[ ]+', '', release_date['release_date'])).strip()
    except Exception:
        infoDict['release_date'] = ''
    try:
        film_length = re.search(
            r'片长:(?P<film_length>[\s\S]*?)\n', info).groupdict()
        infoDict['film_length'] = '%s' % (re.sub(
            '[ ]+', '', film_length['film_length'])).strip()
    except Exception:
        infoDict['film_length'] = ''
    try:
        stra = re.search(r'IMDb链接:(?P<stra>[\s\S]*?)\n', info).groupdict()
        infoDict['stra'] = '%s' % (re.sub(
            '[ ]+', '', stra['stra'])).strip()
    except Exception:
        infoDict['stra'] = ''
    if bs.find('span', class_='all hidden') != None:
        infoDict['introduction'] = bs.find(
            'span', class_='all hidden').get_text().strip()
    elif bs.find('div', attrs={'id': "link-report"}) != None:
        infoDict['introduction'] = bs.find(
            'span', attrs={'property': "v:summary"}).get_text().strip()
    else:
        infoDict['introduction'] = ''
    try:
        infoDict['common_label'] = '\t'.join([a.get_text() for a in bs.find(
            'div', class_='tags-body').select('a')])
    except Exception:
        infoDict['common_label'] = ''
    try:
        see_string = bs.find(
            'div', class_='subject-others-interests-ft').select('a')[0].get_text()
        want_see_string = bs.find(
            'div', class_='subject-others-interests-ft').select('a')[1].get_text()
        pattern = re.compile(r'\d+')   # 查找数字
        infoDict['seen_quantity'] = int(pattern.findall(see_string)[0])
        infoDict['want_to_see'] = int(pattern.findall(want_see_string)[0])
    except Exception:
        infoDict['seen_quantity'] = ''
        infoDict['want_to_see'] = ''
    print(infoDict)
    return infoDict


def getUrl():
    if os.path.isfile('../url/url0.txt'):
        print('已存在！！！')
        return None
    with open('douban.json', 'r', encoding='utf-8') as jsonFile:
        jsonData = jsonFile.read()
        jsonList = json.loads(jsonData)
        url = []
        for i in range(len(jsonList)):
            url.append(jsonList[i]['subject'])
            if not os.path.isdir('../url'):
                os.makedirs('../url')
            with open('../url/url%s.txt' % (i//1000), 'a', encoding='utf-8') as getallurl:
                getallurl.write(jsonList[i]['subject'] + '\n')
            print(jsonList[i]['subject'])
    return jsonList


def get_all(i):
    FileName = 'url%s.txt' % i
    with open('../url/%s' % FileName, 'r', encoding='utf-8') as urlFile:
        urlList = urlFile.read().split('\n')
    if urlList[0] == '':
        return 'Next'
    url = urlList.pop(0)
    infoDict = getHtmlMessage(url)
    if infoDict != None:
        if not os.path.isdir('../info'):
            os.makedirs('../info')
        with open('../info/info%s.txt' % (i), 'a', encoding='utf-8') as getallurl:
            getallurl.write(str(infoDict) + '\n')
    else:
        pass
    if infoDict != None:
        for key, value in infoDict.items():
            if key == 'subject':
                continue
            v = re.sub(r"[']+", "\\'", str(
                value))
            sql = "UPDATE `film_list` SET `" + \
                str(key) + "` = '" + v + \
                "' WHERE `film_list`.`subject` = " + str(url) + ";"
            print(sql)
            if not os.path.isdir('../sql'):
                os.makedirs('../sql')
            with open('../sql/update%s.sql' % i, 'a', encoding='utf-8')as sqlFile:
                sqlFile.write(sql + '\n')
    os.remove('../url/%s' % FileName)
    for u in urlList:
        with open('../url/%s' % FileName, 'a', encoding='utf-8')as urlFile:
            urlFile.write(u + '\n')
    get_all(i)


if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(1000000)
    # getUrl()
    i = 0
    while True:
        getall = get_all(i)
        if getall == 'Next':
            i = i + 1
            if i == 17:
                break
        else:
            continue