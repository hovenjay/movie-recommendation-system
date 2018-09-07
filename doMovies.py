""" Recommendation algorithm | 推荐算法 """
from operator import itemgetter
from jieba import posseg, analyse
from dbo import get_film, get_films

# 相似推荐：
# 根据一页电影信息，推荐相似电影


def similar_films(like: str, sort: str, page: int) -> list:
    # 参数传入一页共 30 部电影，类型为 tuple
    # 返回一个包含五部电影信息的字典
    recomlist = []  # 初始化推荐的电影的列表
    if not get_films(like, sort, page):  # 如果当前页没有内容，返回空列表
        return recomlist
    page = page + 1
    if not get_films(like, sort, page):  # 如果当前页的下一页没有内容，基于倒数第三页进行推荐
        page = page - 3
    films = get_films(like, sort, page)  # 获取全部电影信息
    notes = {}
    for info in films:  # 将每部电影的信息拼接成一个字符串
        if info[0] not in notes:  # 基于电影ID，电影名称，又名，导演，主演，类型，标签
            notes.setdefault(info[0], [])
        notes[info[0]] = str(info[0]) + str(info[1]) + str(info[2]) + str(
            info[3]) + str(info[5]) + str(info[6]) + str(info[14])
    stop_words = []  # 读取停止字到列表中
    with open('./data/stop_words.txt', 'rb') as obj:
        stop_words = obj.readlines()
    key_words = []
    for i, (mvn, word) in enumerate(notes.items()):
        if i > 9:
            break
        words = posseg.cut(word)
        for wds in words:
            if wds.flag.startswith('n') and wds.word not in stop_words:
                key_words.append(wds.word)
    resultWord = analyse.extract_tags(str(key_words), topK=6)
    other_film_words = {}
    for i, (mvn, oword) in enumerate(notes.items()):
        if i <= 9:
            continue
        keys = []
        owords = posseg.cut(oword)
        for owds in owords:
            if owds.flag.startswith('n') and owds.word not in stop_words:
                keys.append(owds.word)
        if mvn not in other_film_words:
            other_film_words.setdefault(mvn, [])
        other_film_words[mvn] = analyse.extract_tags(str(keys), topK=4)
    recommendfilms = {}
    for mvn, r in other_film_words.items():
        if mvn not in recommendfilms:
            recommendfilms.setdefault(mvn, 0)
        recommendfilms[mvn] = len(set(r) & set(resultWord)) / len(resultWord)
    mvlist = sorted(
        recommendfilms.items(), key=itemgetter(1), reverse=True)[:6]
    for i in mvlist:
        temp = get_film(i[0])
        recomlist.append(temp)
    return recomlist


def main():
    recomlist = similar_films('科幻', '', 59)
    for i in recomlist:
        print(i[0])


if __name__ == '__main__':
    main()
