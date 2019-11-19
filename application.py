import os

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
engine = create_engine(os.getenv("DATABASE_URL"))
# Set up database
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return  render_template("logPage.html")

@app.route("/welcome", methods=["GET","POST"])
def welcome():
    if request.method=="POST":
        session.name = request.form.get("name")
        session.contrasena = request.form.get("psw")
        name = request.form.get("name")
        contrasena = request.form.get("psw")
        return  render_template("welcome.html",
        name=session.name,
        contrasena=session.contrasena)
    else:
        return render_template(" advertencia.html")

@app.route("/welcomeNewUser")
def welcomeNewUser():
    return  render_template("welcomeNewUser.html")

# @app.route("/welcomeNewUser/portal")
# def portal():
#     return  render_template("portal.html")
