from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__= "users"
    user = db.Column(db.String, primary_key=True)
    password =db.Column(db.String, nullable=False)
    # def __init__(self,user,password):

        # self.user = user
        # counter += 1
        # self.password = password

# sbnNumber,title,author,year
class Book(db.Model):
    __tablename__= "books"
    sbnNumber = db.Column(db.String, primary_key = True)
    title = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)
    pubYear = db.Column(db.String, nullable = False)
    # bookCounter = 1
    # def __init__(self,sbnNumber,title,author,pubYear):
    #     self.sbnNumber =sbnNumber
    #     bookCounter += 1
    #     self.title = title
    #     self.author = author
    #     self.pubYear =pubYear
#
# class Review(db.Model):
#     __tablename__="reviews"
#     sbnNumber = db.Column(db.String,db.ForeignKey("books.sbnNumber"))
#     user = db.Column(db.String, db.ForeignKey("users.user"))
#     comentario= db.Column(db.String)
#     rate= db.Column(db.String)

    # reviewCounter = 1

    # def __init__(self,sbnNumber,comentario,rate):
    #     self.sbnNumber =sbnNumber
    #     self.comentario = comentario
    #     self. rate=rate
