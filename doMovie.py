import dbo
import re
from operator import itemgetter
import random
import math


def getFilmDict(sub):
    movie = dbo.get_film(sub)
    if movie is None:
        return None
    # print(movie)
    movieDict = {}
    if movie[0] != '' and movie[0] is not None:
        movieDict['subject'] = movie[0]
    if movie[1] != '' and movie[1] is not None:
        movieDict['title'] = movie[1]
    if movie[2] != '' and movie[2] is not None:
        movieDict['alias'] = movie[2].split('{}')
    if movie[3] != '' and movie[3] is not None:
        movieDict['director'] = movie[3].split('{}')
    if movie[4] != '' and movie[4] is not None:
        movieDict['writer'] = movie[4].split('{}')
    if movie[5] != '' and movie[5] is not None:
        movieDict['starring'] = movie[5].split('{}')
    if movie[6] != '' and movie[6] is not None:
        movieDict['classification'] = movie[6].split('{}')
    if movie[7] != '' and movie[7] is not None:
        movieDict['country'] = movie[7].split('{}')
    if movie[8] != '' and movie[8] is not None:
        movieDict['language'] = movie[8].split('{}')
    if movie[9] != '' and movie[9] is not None:
        movieDict['score'] = movie[9]
    if movie[10] != '' and movie[10] is not None:
        movieDict['ratio'] = re.sub('好于 ', '', movie[10]).split('{}')
    if movie[11] != '' and movie[11] is not None:
        movieDict['release_date'] = movie[11].split('/')
    if movie[12] != '' and movie[12] is not None:
        movieDict['film_length'] = movie[12].split('/')
    if movie[13] != '' and movie[13] is not None:
        movieDict['introduction'] = re.sub('\n+', '<br/>', movie[13])
    if movie[14] != '' and movie[14] is not None:
        movieDict['common_label'] = movie[14].split('{}')
    if movie[15] != '' and movie[15] is not None:
        movieDict['seen_quantity'] = movie[15]
    if movie[16] != '' and movie[16] is not None:
        movieDict['want_to_see'] = movie[16]
    if movie[18] != '' and movie[18] is not None:
        movieDict['vister'] = movie[18]
    if movie[20] != '' and movie[20] is not None:
        movieDict['IMDb'] = movie[20]
    if movie[21] != '' and movie[21] is not None:
        movieDict['strb'] = movie[21]
    try:
        movieDict['year'] = re.findall('\d{4}-', movie[11])[0][:4]
    except Exception:
        movieDict['year'] = ''
    if movieDict['year'] == '':
        del movieDict['year']
    return movieDict


def addVited(sub, userName):
    user = dbo.get_user(userName)
    vited = user['viewed']
    # print(user)
    if str(sub) not in vited:
        v = vited + '-' + str(sub)
        sql = "UPDATE `user_list` SET `viewed` = '%s' WHERE `user_list`.`uname` = '%s';" % (
            v, userName)
        dbo.query(sql)
        # print('Add_True')
        return True
    else:
        # print('Add_False')
        return False


def recommendMovies(subject):
    us = dbo.get_users()
    user_movies_matrix = {}
    for u in us:
        if u[0] not in user_movies_matrix:
            user_movies_matrix.setdefault(u[0], [])
        visted = u[3].split('-')
        if visted[-1] == '':
            visted.pop(-1)
        user_movies_matrix[u[0]] = visted
    # print(user_movies_matrix)
    # 获取看过的用户有哪些
    users = []
    for user, movies in user_movies_matrix.items():
        if str(subject) in movies:
            users.append(user)
    # print(users)
    movies_inter = {}
    for user in users:
        for movie in user_movies_matrix[user]:
            if movie == str(subject):
                continue
            if movie not in movies_inter:
                movies_inter.setdefault(movie, 0)
            movies_inter[movie] += 1
    # print(movies_inter)
    # print(sorted(movies_inter.items(), key=itemgetter(1), reverse=True)[:20])
    suggestMovie = []
    for sub, inter in sorted(
            movies_inter.items(), key=itemgetter(1), reverse=True)[:10]:
        movie = dbo.get_film(int(sub))
        suggestMovieDict = {}
        suggestMovieDict['title'] = movie[1][:movie[1].find(' ')]
        suggestMovieDict['strb'] = movie[21]
        suggestMovieDict['subject'] = sub
        suggestMovie.append(suggestMovieDict)
    # print(suggestMovie)
    if len(users) >= 5:
        suggestUser = [random.choice(users) for i in range(2)]
        # print(suggestUser)
        vistedUsers = [
            dbo.get_user(suggestUser[0])['uname'],
            dbo.get_user(suggestUser[1])['uname']
        ]
        return suggestMovie, vistedUsers
    return suggestMovie


def SamerLiker(userName, nowVisted, topN=2, topK=5):
    us = dbo.get_users()
    # 获得用户电影矩阵
    user_movies_matrix = {}
    for u in us:
        if u[0] not in user_movies_matrix:
            user_movies_matrix.setdefault(u[0], [])
        visted = u[3].split('-')
        if visted[-1] == '':
            visted.pop(-1)
        user_movies_matrix[u[0]] = visted
    # print(user_movies_matrix)
    movies_user_matrix = {}
    user_inter_matrix = {}
    user_similar_matrix = {}
    # 矩阵翻转
    for user, movs in user_movies_matrix.items():
        for mov in movs:
            if mov not in movies_user_matrix:
                movies_user_matrix.setdefault(mov, set())
            movies_user_matrix[mov].add(user)
    # print(movies_user_matrix)
    # 统计每个人和其他人观看相同影片次数
    for mov, users in movies_user_matrix.items():
        for user in users:
            for user2 in users:
                if user == user2:
                    continue
                if user not in user_inter_matrix:
                    user_inter_matrix.setdefault(user, {})
                if user2 not in user_inter_matrix[user]:
                    user_inter_matrix[user][user2] = 0
                user_inter_matrix[user][user2] += 1
    # print(user_inter_matrix)
    # 计算每个人之间的相互重叠内容的比例
    for user, usercount in user_inter_matrix.items():
        for user2, inter in usercount.items():
            if user not in user_similar_matrix:
                user_similar_matrix.setdefault(user, {})
            if user2 not in user_similar_matrix[user]:
                user_similar_matrix[user][user2] = 0
            user_similar_matrix[user][user2] = inter / math.sqrt(
                len(user_movies_matrix[user]) * len(user_movies_matrix[user2]))
    # print(user_similar_matrix)
    # 获取和登陆者看过内容最相近2人
    # print(sorted(user_similar_matrix[userName].items(), key=itemgetter(1), reverse=True)[:2])
    vistedMovie = user_movies_matrix[userName]
    recommendMovies = {}
    # 根据最相近的TOPN个人进行计算
    for user, usercount in sorted(
            user_similar_matrix[userName].items(), key=itemgetter(1),
            reverse=True)[:topN]:
        # print('user: %s\t, usercount: %s' % (user, usercount))
        for mov in user_movies_matrix[user]:
            if mov in vistedMovie:
                continue
            # print(mov)
            if mov not in recommendMovies:
                recommendMovies.setdefault(mov, 0)
            recommendMovies[mov] += usercount
    # print(sorted(recommendMovies.items(), key=itemgetter(1), reverse=True)[:topK])
    SamerLikeMovies = []
    for sub, inter in sorted(
            recommendMovies.items(), key=itemgetter(1), reverse=True)[:topK]:
        if sub == str(nowVisted):
            continue
        movie = dbo.get_film(int(sub))
        SamerLikeMoviesDict = {}
        SamerLikeMoviesDict['title'] = movie[1][:movie[1].find(' ')]
        SamerLikeMoviesDict['strb'] = movie[21]
        SamerLikeMoviesDict['subject'] = sub
        SamerLikeMovies.append(SamerLikeMoviesDict)
    # print(SamerLikeMovies)
    return SamerLikeMovies[:4]


if __name__ == '__main__':
    # for key,value in getFilmDict(1291543).items():
    #     print(key,':',value)
    # recommendMovies(1291543)
    # recommendMovies(3338821)
    SamerLiker('March', 1291543)
