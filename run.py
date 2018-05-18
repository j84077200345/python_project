from flask import Flask, render_template, request, session, redirect
from models import item
from models.user import User
from models.video import Video
from common.database import Database

app = Flask(__name__)
app.secret_key = "j84077200345"

@app.before_first_request
def init_db():
    Database.initialize()
    session['Account'] = session.get('account')
    session['Name'] = session.get('name')

@app.route("/")
def hello():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login_method():
    if request.method == 'POST':
        account = request.form['InputAccount']
        password = request.form['InputPassword']
        check = User.is_login_valid(account, password)
        if check is True:
            session['Account'] = account
            session['Name'] = User.find_user_data(account).get('Name')
            return redirect("/")
        else:
            message = "Your account or password is wrong !!"
            return render_template("login.html", message=message)
    else:
        return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register_method():
    if request.method == 'POST':
        name = request.form['InputName']
        account = request.form['InputAccount']
        password = request.form['InputPassword']
        result = User.register_user(name, account, password)
        if result is True:
            session['Account'] = account
            session['Name'] = User.find_user_data(account).get('Name')
            return redirect("/")
        else:
            message = "Your account is already exist !!"
            return render_template("register.html", message=message)
    else:
        return render_template("register.html")

@app.route("/logout")
def logout_method():
    session['Account'] = not session['Account']
    return redirect("/")

@app.route("/result")
def result_page():
    favorite_video = []
    user_favorite = Video.find_video(session['Account'])
    for video in user_favorite:
        favorite_video.append(video['link'])

    url = request.url
    search = request.args.get('search')
    soup = item.find_search_content(search)
    all_item = item.every_video(soup)
    return render_template("result.html", search=search, all_item=all_item, url=url, favorite_video=favorite_video)

@app.route("/favorite", methods=['GET', 'POST'])
def favorite_method():
    if session['Account']:
        if request.method == 'POST':
            url = request.form['url']
            title = request.form['title']
            link = request.form['link']
            img = request.form['img']
            account = session['Account']
            Video(account, title, link, img).save_to_db()
            return redirect(url)
        else:
            account = session['Account']
            user_video = Video.find_video(account)
            return render_template("favorite.html", user_video=user_video)
    else:
        return redirect("/login")

@app.route("/delete", methods=['POST'])
def delete_method():
    link = request.form['link']
    account = session['Account']
    Video.delete_video(account, link)
    return redirect("/favorite")

@app.route("/download")
def download():
    value = request.args.get('value')
    download_type, url = value.split("&")
    if download_type == "MP3":
        item.download_mp3(url)
        return render_template("download.html")
    elif download_type == "MP4":
        item.download_mp4(url)
        return render_template("download.html")

if __name__ == "__main__":
    app.run(debug=True, port=4460)