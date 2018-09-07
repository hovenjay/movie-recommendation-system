import doMovie
from doMovies import similar_films
from flask import Flask, render_template, redirect, url_for, request, session, escape, json
from dbo import user_login, get_films
app = Flask(__name__)
# app.config['DEBUG'] = True  # 开启 debug 模式
app.config['SECRET_KEY'] = 'hONyY9FjRvQH'  # 加密令牌


def user_is_logged():  # 校验 session 中存储的用户信息是否有效
    msg = {'result': False, 'info': 'session 不正确或不存在'}
    if 'username' in session and 'password' in session:
        username = escape(session['username'])
        password = escape(session['password'])
        msg = user_login(username, password)  # 校验 Cookie 存储的信息是否正确
        return msg
    else:
        session.clear()
        return msg


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/subject/<int:sub>/')
def subject(sub):
    msg = user_is_logged()
    same_like_movie = None
    movie = doMovie.getFilmDict(sub)
    if movie is None:
        return render_template('404.html')
    if msg['result']:
        username = escape(session['username'])
        same_like_movie = doMovie.SamerLiker(username, sub)
    suggest = doMovie.recommendMovies(sub)
    if type(suggest) == tuple:
        suggestMovie = suggest[0]
        vistedUsers = suggest[1]
        return render_template(
            'detailsPage.html',
            movie=movie,
            suggestMovie=suggestMovie,
            vistedUsers=vistedUsers,
            same_like_movie=same_like_movie)
    suggestMovie = suggest
    return render_template(
        'detailsPage.html',
        movie=movie,
        suggestMovie=suggestMovie,
        same_like_movie=same_like_movie)


@app.route('/addVited/<int:sub>')
def addVited(sub):
    msg = user_is_logged()
    if msg['result']:
        username = escape(session['username'])
        doMovie.addVited(sub, username)
    return redirect(url_for('subject', sub=sub))


@app.route('/show_uname', methods=['GET', 'POST'])
def show_uname():
    if request.method == 'GET':
        return render_template('404.html')
    else:
        msg = user_is_logged()
        if msg['result']:
            msg['info'] = escape(session['username'])
        else:
            msg['info'] = '提示：用户名不存在！'
        return json.dumps(msg)


@app.route('/show_films', methods=['GET', 'POST'])
def show_films():
    if request.method == 'GET':
        return render_template('404.html')
    else:
        like = request.values.get('like')
        sort = request.values.get('sort')
        page = request.values.get('page')
        films = get_films(like, sort, int(page))
        return json.dumps(films)


@app.route('/show_recomm', methods=['GET', 'POST'])
def show_recomm():
    if request.method == 'GET':
        return render_template('404.html')
    else:
        like = request.values.get('like')
        sort = request.values.get('sort')
        page = request.values.get('page')
        films = similar_films(like, sort, int(page))
        return json.dumps(films)


@app.route('/login', methods=['GET'])
def login():
    msg = user_is_logged()
    if msg['result']:
        return redirect(url_for('index'))
    else:
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_form():
    username = request.values.get('username')
    password = request.values.get('password')
    msg = user_login(username, password)
    if msg['result']:
        session['username'] = username
        session['password'] = password
        return redirect(url_for('index'))
    else:
        message = "提示：" + msg['info'] + "，请重新输入！"
        return render_template('login.html', message=message)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('password', None)
    # session.clear()
    return redirect(url_for('index'))


@app.errorhandler(404)  # 404页面
def page_not_found(error):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
