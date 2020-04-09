import os
import requests

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

api_key = "6SW4uW5WvXThNV8UmMlCfg"
res = requests.get(f"https://www.goodreads.com/search.xml?key={api_key}&q=Ender%27s+Game")

print('res: ', res)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    db.execute("INSERT INTO ")
    email = request.form.get("email")
    password = request.form.get("password")
    print(email)
    print(password)
    return render_template("success.html", email=email, password=password, message="Successfully registered!")
