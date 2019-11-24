import os

from flask import Flask, session, render_template, request, redirect
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
#    session["books"]=db.execute("""SELECT "sbnNumber","title","author", "pubYear" FROM "books" WHERE "title" LIKE :tito AND "pubYear" LIKE :yer AND "author" LIKE :crea AND "sbnNumber" LIKE :num""",
#    {"tito":integra(session["title"]),"yer":integra(session["pubYear"]),"crea":integra(session["author"]),"num":integra(session["sbnNumber"])}).fetchall()
    # if request.method=="POST":
        # return  render_template("searchPage.html",books=session["books"],mensaje="post")#session["books"],mensaje="posted")

    # if session["books"] is None:
    #     return "bool" #render_template("searchPage.html",bks=session["books"],mensaje="no existe ese libro",psw=session["password"],name=session["user"])

    return render_template("searchPage.html",bks=session["books"],
    lol=session["sbnNumber"],
    psw=session["password"],
    name=session["user"])
    #,mensaje=" busqueda exitosa")

@app.route("/searchPage/<Source>", methods=["GET","POST"] )
def bookdata(Source):
    session["review"]=request.form.get("review")
    session["rate"]=request.form.get("rate")
    session["datareview"]=""
    session["databook"]=db.execute("""SELECT * FROM "books" WHERE "sbnNumber" = :Source""",{"Source":Source}).fetchone()
    if session["databook"] is None:
        return  render_template("error.html",mensaje="no disponemos de este libro")
    session["datareview"] = db.execute("""SELECT * FROM "reviews" WHERE "sbnNumber" = :Sour""",{"Sour":Source}).fetchall()
    #return "sssssssssss"# render_template("review.html",book=session["databook"],reviews=session["datareview"],rates=[1,2,3,4,5])#,sbnN=Source)
    session["review"]=request.form.get("review")

    session["rate"]=request.form.get("rate")
    if session["review"] is None:
        return  render_template("review.html",book=session["databook"],reviews=session["datareview"],rates=[1,2,3,4,5],sbnN=Source)
    print("""INSERT INTO "reviews" ("user","sbnNumber","comentario","rate") VALUES  (:name , :source,:review,:rate) """,{"name":session["name"],"source":Source,"review":session["review"],"rate":session["rate"]})
    db.execute("""INSERT INTO "reviews" ("user","sbnNumber","comentario","rate") VALUES  (:name , :source,:review,:rate) """,{"name":session["name"],"source":Source,"review":session["review"],"rate":session["rate"]})
    db.commit()
    session["databook"]=db.execute("""SELECT * FROM "books" WHERE "sbnNumber" = :Source""",{"Source":Source }).fetchone()
    if session["databook"] is None:
        return  render_template("error.html",mensaje="no disponemos de este libro"),404
        session["datareview"] = db.execute("""SELECT * FROM "reviews" WHERE "sbnNumber" = :Sour""", {"Sour":Source }).fetchall()
    return  render_template("review.html",book=session["databook"],reviews=session["datareview"],rates=[1,2,3,4,5],sbnN=Source)

    #render_template("advertencia.html",sbnNum=Source)

# @app.route("/welcomeNewUser/portal")
# def portal():
#     return  render_template("portal.html")
