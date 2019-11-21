import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    books = Book.query.all()
    for book in books:
        print(f"added {book.sbnNumber} - {book.title},From {book.author} created {book.pubYear}")

if __name__ == "__main__":
    with app.app_context():
        main()
