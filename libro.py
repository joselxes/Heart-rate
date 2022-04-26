import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
def integra( palabra):
    add='%'
    return add+palabra+add
def main():

    # List all flights.
    # books =db.execute("""SELECT "sbnNumber","title","author", "pubYear" FROM "books" """).fetchall()
    #
    # for book in books:
    #     print(f"LIBRO {book.sbnNumber}:TITULO -{book.title}")
    #     print(f" autor {book.author}, ano {book.pubYear} .")

#SELECT "sbnNumber", "title","author","pubYear"
#FROM "books"
#WHERE "title" LIKE '%The%' AND "pubYear" LIKE '%2%' AND "author" LIKE '%o%' AND "sbnNumber" LIKE '%X%'
#LIMIT 50
app = Flask(__name__)
def integra( palabra):
    add='%'
    return add+palabra+add
    session["sbnNumber"] = request.form.get("sbnNumber")
    session["title"] = request.form.get("title")
    session["author"] = request.form.get("author")
    session["pubYear"] = request.form.get("pubYear")
    boks =db.execute("""SELECT "sbnNumber","title","author", "pubYear" FROM "books" WHERE "title" LIKE :tito AND "pubYear" LIKE :yer AND "author" LIKE :crea AND "sbnNumber" LIKE :num""",
    {"tito":integra(session["title"]),"yer":integra(session["pubYear"]),"crea":integra(session["author"]),"num":integra(session["sbnNumber"])}).fetchall()

//
    yyy="2"
    yer=integra(yyy)
    tito=integra("h")
    num=integra("%2")
    crea=integra("%h%")
    boks =db.execute("""SELECT "sbnNumber","title","author", "pubYear" FROM "books" WHERE "title" LIKE :tito AND "pubYear" LIKE :yer AND "author" LIKE :crea AND "sbnNumber" LIKE :num""",{"tito":tito,"yer":yer,"crea":crea,"num":num}).fetchall()
    for bok in boks:
        print(f"LIBRO {bok.sbnNumber}:TITULO -{bok.title}")
        print(f" autor {bok.author}, ano {bok.pubYear} .")
    print(yer)
    # Prompt user to choose a flight.

    # Make sure flight is valid.
    # if flight is None:
    #     print("Error: No such flight.")
    #     return
    #
    # # List passengers.
    # passengers = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
    #                         {"flight_id": flight_id}).fetchall()
    # print("\nPassengers:")
    # for passenger in passengers:
    #     print(passenger.name)
    # if len(passengers) == 0:
    #     print("No passengers.")

if __name__ == "__main__":
    main()
