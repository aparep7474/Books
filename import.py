import csv, os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine ("DATABASE_URL")
db = scoped_session(sessionmaker(bind=engine))

def main():
    file = open("books.csv")
    reader = csv.reader(file)
    for ISBN, title, author, year in reader:
        db.execute("INSERT INTO books (ISBN, title, author, year)      VALUES (:ISBN, :title, :author, :year)",
       {"ISBN":ISBN, "title":title, "author":author, "year":year})
    db.commit()

if __name__ == "__main__":
    main()
