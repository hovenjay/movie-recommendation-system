# 从网络获取英文名称列表
import requests
from bs4 import BeautifulSoup
import time
import re


def getUrl():
    for a in range(26):
        for i in range(10):
            url = 'http://www.resgain.net/english_names_%s_%s.html' % (
                chr(97 + a), i + 1)
            yield url


def getName(url):
    html = requests.get(url)
    bs = BeautifulSoup(html.text, 'lxml')
    trName = bs.find('tbody').find_all('tr')
    NameList = []
    for i, Name in enumerate(trName):
        if i % 2 == 1:
            continue
        print(Name.td.text)
        if Name.td.text == '':
            continue
        NameList.append(Name.td.text)

    print(NameList)
    return NameList


if __name__ == "__main__":
    for url in getUrl():
        print(url)
        time.sleep(2)
        NameList = getName(url)
        with open('NameList.txt', 'a', encoding='utf-8') as obj:
            for name in NameList:
                obj.write(name + '\n')
    # getName("http://www.resgain.net/english_names_z_3.html")