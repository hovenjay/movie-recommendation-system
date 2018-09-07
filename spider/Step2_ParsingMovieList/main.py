# 读取从数据库导出的 douban.json 文件，生成每部电影的详细信息页的链接列表
import json


def write_to_file(fileName, s: str):
    f = open('./message/%s' % fileName, 'a', encoding='utf-8')
    f.write(s)
    f.close()


def getUrl():
    with open('douban.json', 'r', encoding='utf-8') as jsonFile:
        jsonData = jsonFile.read()
        jsonList = json.loads(jsonData)
        url = []
        for i in range(len(jsonList)):
            url.append(jsonList[i]['subject'])
            write_to_file('%s.txt' % (i // 1000),
                          jsonList[i]['subject'] + '\n')
    return jsonList


if __name__ == '__main__':
    getUrl()
