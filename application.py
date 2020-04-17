import os
import requests
from models import *

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

api_key = "6SW4uW5WvXThNV8UmMlCfg"
res = requests.get(f"https://www.goodreads.com/search.xml?key={api_key}&q=Ender%27s+Game")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    password = request.form.get("password")

    if db.execute("SELECT * FROM users WHERE email = :email", {"email": email}).rowcount == 1:
        return render_template("error.html", message="Email already exsists")
    db.execute("INSERT INTO users (email, password) VALUES(:email, :password)", {"email": email, "password": password})

    db.commit()
    return render_template("success.html", email=email, password=password, message="Successfully registered!")


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("login_email")
    password = request.form.get("login_password")

    if db.execute("SELECT * FROM users WHERE email = :email AND password = :password", {"email": email, "password":
        password}).rowcount == 0:
        return render_template("error.html", message="Please register for an account")
    else:
        return render_template("login.html", email=email)


@app.route("/search", methods=["POST"])
def search():
    search = request.form.get("search")

    res = db.execute("SELECT * FROM books WHERE title = :title OR author = :author OR isbn = :isbn OR year = :year",
                     {
                         "title": search,
                         "author": search,
                         "isbn": search,
                         "year": search
                     }).fetchall()

    return render_template("login.html", res=res)


@app.route("/detail/<int:book_id>")
def detail(book_id):
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()

    reviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {
        "book_id": book_id
    })

    return render_template("book.html", book=book, reviews=reviews)


@app.route("/review/<int:book_id>", methods=["POST"])
def review(book_id):
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()

    rating = request.form.get("rating")
    review = request.form.get("review")

    db.execute("INSERT INTO reviews (rating, review, book_id) VALUES (:rating, :review, :book_id)",
               {"rating": rating, "review": review, "book_id": book_id})

    db.commit()

    # book_review = db.exectue("SELECT * FROM reviews WHERE book_id = :book_id",
    #                          {"book_id": book_id})

    print("book: ", book)

    return render_template("review_added.html", message="Success")
