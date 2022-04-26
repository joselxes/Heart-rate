import csv
import os

from flask import Flask, render_template, request
from models import *


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    f=open("books.csv")
    reader = csv.reader(f)
    for sbnNumber,title,author,pubYear in reader:
        book = Book(sbnNumber=sbnNumber, title=title, author=author, pubYear=pubYear)
        db.session.add(book)
        print(f"added book {sbnNumber} - {title},From {author} created {pubYear}")
    db.session.commit()
if __name__ == "__main__":
    with app.app_context():
        main()
