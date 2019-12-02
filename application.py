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
    session["password"]=request.form.get("psw")
    session["user"]=request.form.get("name")
    nombre=session["user"]
    session["cliente"] = db.execute("""SELECT * FROM "users" WHERE "user" = :user""", {"user":session["user"] }).fetchone()
    if session.get("cliente") is None:
            return  render_template("trueLogin.html")
    if session["cliente"].password != session["password"]:
                return  render_template("trueLogin.html")
    if session.get("books") is None:
        session["title"]=""
        session["pubYear"]=""
        session["author"]=""
        session["sbnNumber"]=""
        session["books"]=""#db.execute("""SELECT "sbnNumber","title","author", "pubYear" FROM "books" WHERE "title" LIKE :tito AND "pubYear" LIKE :yer AND "author" LIKE :crea AND "sbnNumber" LIKE :num""",
#        {"tito":integra(session["title"]),"yer":integra(session["pubYear"]),"crea":integra(session["author"]),"num":integra(session["sbnNumber"])}).fetchall()
    clienteFijo=session["user"]
    session["title"]=request.form.get("title")
    session["pubYear"]=request.form.get("pubYear")
    session["author"]=request.form.get("author")
    session["sbnNumber"]=request.form.get("sbnNumber")
    comando=["""SELECT "sbnNumber","title","author", "pubYear" FROM "books" WHERE "title" LIKE :tito AND "pubYear" LIKE :yer AND "author" LIKE :crea AND "sbnNumber" LIKE :num""",{"tito":integra(session["title"]),"yer":integra(session["pubYear"]),"crea":integra(session["author"]),"num":integra(session["sbnNumber"])}]
    print(comando)
    session["books"]=db.execute("""SELECT "sbnNumber","title","author", "pubYear" FROM "books" WHERE "title" LIKE :tito AND "pubYear" LIKE :yer AND "author" LIKE :crea AND "sbnNumber" LIKE :num""",{"tito":integra(session["title"]),"yer":integra(session["pubYear"]),"crea":integra(session["author"]),"num":integra(session["sbnNumber"])}).fetchall()

    return render_template("searchPage.html",bks=session["books"],
    lol=session["sbnNumber"],
    psw=session["password"],
    name=session["user"])
    #,mensaje=" busqueda exitosa")

@app.route("/searchPage/<Source>", methods=["GET","POST"] )
def bookdata(Source):
    session["name"]=request.form.get("name")
    print("---------------------------------")
    print(session["name"])
    print("---------------------------------")
    session["review"]=request.form.get("review")
    session["rate"]=request.form.get("rate")
    session["databook"]=db.execute("""SELECT * FROM "books" WHERE "sbnNumber" = :Source""",{"Source":Source}).fetchone()
    if session["databook"] is None:
        return  render_template("error.html",mensaje="no disponemos de este libro"),404

    session["datareview"] = db.execute("""SELECT * FROM "reviews" WHERE "sbnNumber" = :Sour""",{"Sour":Source}).fetchall()

    if session["review"] is None:
        return  render_template("review.html",book=session["databook"],reviews=session["datareview"],rates=[1,2,3,4,5],sbnN=Source,name=session["name"],nope="caso vacio")


#    session["rate"]=request.form.get("rate")
    print("""INSERT INTO "reviews" ("user","sbnNumber","comentario","rate") VALUES  (:name , :source,:review,:rate) """,{"name":session["name"],"source":Source,"review":session["review"],"rate":session["rate"]})
    try:
        db.execute("""INSERT INTO "reviews" ("user","sbnNumber","comentario","rate") VALUES  (:name , :source,:review,:rate) """,{"name":session["name"],"source":Source,"review":session["review"],"rate":session["rate"]})
    except :
        return  render_template("error.html",mensaje="no puede realizar otro comentario"),404
    db.commit()
    session["datareview"] = db.execute("""SELECT * FROM "reviews" WHERE "sbnNumber" = :Sour""", {"Sour":Source }).fetchall()

    return  render_template("review.html",book=session["databook"],reviews=session["datareview"],rates = [1,2,3,4,5],sbnN=Source,name=session["name"])

@app.route("/api/searchPage/<Source>" )
def bookAPI(Source):

    session["datareview"]=""
    session["databook"]=db.execute("""SELECT * FROM "books" WHERE "sbnNumber" = :Source""",{"Source":Source}).fetchone()
    if session["databook"] is None:
        return jsonify({"error":"invalid requested book "}),404
    session["res"] = requests.get("https://www.goodreads.com/book/review_counts.json",params={"key": "XpBeTod1UwDEF989WE4g", "isbns": Source})
    session["data"]=session["res"].json()
    #rate=data["books"][0]["work_ratings_count"]
    #rate1=data["books"][0]["average_rating"]
    return jsonify({
    "title": session["databook"].title,
    "author": session["databook"].author,
    "year": session["databook"].pubYear,
    "isbn": session["databook"].sbnNumber,
    "review_count":session["data"]["books"][0]["work_ratings_count"],
    "average_score":session["data"]["books"][0]["average_rating"]
    })
