import os
import requests
from flask import Flask, session, render_template, request, redirect, jsonify
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
def integra( palabra):
    add='%'
    return add+palabra+add
def integr( palabra):
    add=' '
    return add+palabra+add
# def confirma( palabra):
#     if palabra is None:
#         return "u"
#     return palabra

@app.route("/",methods=["GET","POST"])
def index():
    if session.get("name") is None:
        session["name"] = []
        session["contrasena"] = ""
        session["session"] = "si"
    # book = Book(sbnNumber=sbnNumber, title=title, author=author, pubYear=pubYear)
    # db.session.add(book)
    if request.method == "POST":
        session["session"]=request.form.get("session")
        if session["session"] == "no" :
            session.clear()
            session["name"] = []
            clienteFijo=""
            session["psw"] = ""
            session["session"] = "si"
            return  render_template("trueLogin.html")
        else:
            session["name"] = request.form.get("name")
            session["psw"] = request.form.get("psw")
            db.execute("""INSERT INTO "users" ("user","password") VALUES  (:name , :psw) """, {"name":session["name"],"psw":session["psw"]})
            db.commit()

        # return  render_template("trueLogin.html")

    return  render_template("trueLogin.html")

@app.route("/searchPage", methods=["GET","POST"])
def searchPage():
    return render_template("menuPage.html")

@app.route("/ilumi", methods=["POST"])
def ilumi():
    return render_template("iluminations.html")

@app.route("/text", methods=["POST"])
def text():
    return render_template("texture.html")

@app.route("/guy", methods=["POST"])
def guy():
    return render_template("guymove.html")

@app.route("/sol", methods=["POST"])
def sol():
    return render_template("sunmove.html")

@app.route("/cloud", methods=["POST"])
def cloud():
    return render_template("indexCloud.html")
