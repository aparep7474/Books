import os, requests, json

from flask import Flask, session, redirect, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return render_template("error.html", message="must provide username")

        usercheck = db.execute("SELECT * FROM users WHERE username = :username",
            {"username":request.form.get("username")}).fetchone()

        if usercheck:
            return render_template("error.html", message="username already exist")

        elif not request.form.get("password"):
            return render_template("error.html", message="must provide password")

        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
            {"username":request.form.get("username"),
            "password":request.form.get("password")})
        db.commit()

        return redirect("/")

    else:
        return render_template("sign_up.html")


@app.route("/", methods=["GET", "POST"])
def log_in():

    session.clear()

    username = request.form.get("username")

    password = request.form.get("password")

    if request.method == "POST":

        if not request.form.get("username"):
            return render_template("error.html", message="must provide username")

        elif not request.form.get("password"):
            return render_template("error.html", message="must provide password")

        rows = db.execute("SELECT * FROM users WHERE username = :username",
            {"username": username})

        rows2 = db.execute("SELECT * FROM users WHERE password = :password",
            {"password": password})

        result = rows.fetchone()

        result2 = rows2.fetchone()

        if result == None:
            return render_template("error.html", message="invalid username or password")

        if result2 == None:
            return render_template("error.html", message="invalid username or password")

        session["id"] = result[0]
        session["username"] = result[1]

        session["username"] = username

        return redirect("/search")

    else:
        return render_template("log_in.html")


@app.route("/log_out")
def log_out():

    session.clear()

    return redirect("/")


@app.route("/search", methods=["GET","POST"])
def search():

    username = session.get("username")

    session["books"] = []

    if request.method == "POST":

        search=request.form.get('search')

        if not search:
            return render_template("error.html", message="must search for a book")

        data=db.execute("SELECT * FROM books WHERE author iLIKE '%"+search+"%' OR title iLIKE '%"+search+"%' OR isbn iLIKE '%"+search+"%'").fetchall()

        for x in data:
            session["books"].append(x)
        if len(session["books"]) == 0:
            return render_template("error.html", message="the book you searched for isn't available")

        return render_template("books.html",data=session["books"],username=username)

    else:
     return render_template("search.html")


@app.route("/book/<string:isbn>", methods=["GET","POST"])
def book(isbn):

    username = session.get("username")

    session["reviews"]=[]

    reviewcheck = db.execute("SELECT * FROM reviews WHERE isbn = :isbn AND username= :username",{"username":username,"isbn":isbn}).fetchone()

    if request.method == "POST" and reviewcheck == None:
        review = request.form.get("review")
        rating = request.form.get("rating")

        db.execute("INSERT INTO reviews (isbn, review, rating, username) VALUES (:a,:b,:c,:d)",{"a":isbn,"b":review,"c":rating,"d":username})

        db.commit()

    if request.method == "POST" and reviewcheck!= None:
        return render_template("error.html", message="you can't add another review")

    res = requests.get("https://www.goodreads.com/book/review_counts.json", verify=False, params={"key": "jo7OuVXDBgHAcouWFzdBzg", "isbns": isbn})

    work_ratings_count = res.json()['books'][0]['work_ratings_count']
    average_rating = res.json()['books'][0]['average_rating']

    data = db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn":isbn}).fetchone()

    reviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn",{"isbn":isbn}).fetchall()

    for y in reviews:
        session["reviews"].append(y)

    else:
        return render_template("book_isbn.html",data=data,reviews=session["reviews"],average_rating=average_rating,work_ratings_count=work_ratings_count,username=username)


@app.route("/api/<string:isbn>")
def api(isbn):

    data = db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn":isbn}).fetchone()

    if data == None:
        return render_template("error.html", message="isbn not found")

    res = requests.get("https://www.goodreads.com/book/review_counts.json", verify=False, params={"key": "jo7OuVXDBgHAcouWFzdBzg", "isbns": isbn})

    work_ratings_count = res.json()['books'][0]['work_ratings_count']
    average_rating = res.json()['books'][0]['average_rating']

    x = {
    "title": data.title,
    "author": data.author,
    "year": data.year,
    "isbn": isbn,
    "work_ratings_count": work_ratings_count,
    "average_rating": average_rating
    }

    api=json.dumps(x)

    return render_template("api.html",api=api)
