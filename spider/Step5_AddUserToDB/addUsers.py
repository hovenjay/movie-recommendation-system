# 将从网络获取的英文名作为用户名插入数据库，用户观影记录随机从电影列表生成
from dbo import get_films, query
import random

movieType = ('剧情', '喜剧', '动作', '爱情', '科幻', '动画', '悬疑', '惊悚', '恐怖', '纪录片', '短片',
             '情色', '同性', '音乐', '歌舞', '家庭', '儿童', '传记', '历史', '战争', '犯罪', '西部',
             '奇幻', '冒险', '灾难', '武侠', '古装', '运动', '黑色电影')
sort = ''
with open('NameList.txt', 'r', encoding="utf-8") as obj:
    NameList = obj.read().split('\n')

for userName in NameList:
    mt = [str(random.choice(movieType)) for i in range(5)]
    viewMovie = []
    for like in mt:
        for t in range(2):
            page = random.randint(0, 30)
            result = get_films(like, sort, page)

            for i in result:
                viewMovie.append(i[0])
                print("%s \t %s " % (i[0], i[1]))

    viewed = list(set([str(random.choice(viewMovie)) for i in range(15)]))
    email = userName + '@email.com'
    password = 123
    sql = "INSERT INTO `user_list` (`uname`, `email`, `passwd`,`viewed`) VALUES ('%s','%s','%s','%s')" % (
        userName, email, password, '-'.join(viewed))
    query(sql)