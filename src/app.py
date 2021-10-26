from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from marshmallow import Schema, fields
from os import path

BASE_DIR = path.abspath(path.dirname(__file__))
DB_URI = "sqlite:///" + path.join(BASE_DIR, "db/database.db")

app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    pages = db.Column(db.Integer, nullable=False, unique=True)


class BookSchema(Schema):
    id = fields.Int()
    name = fields.String()
    pages = fields.Int()


@app.route("/")
def index():
    return '<h1 align="center" style="font-family:Helvetica;">Start with: <a href="http://127.0.0.1:5000/api/books">http://127.0.0.1:5000/api/books</a></h1>'


@app.route("/api/books/", methods=["GET"])
def getAllBooks():
    books = Book.query.all()
    bookSchema = BookSchema(many=True)
    results = bookSchema.dump(books)

    return jsonify(results)


@app.route("/api/books/<string:name>", methods=["GET"])
def getOneBookByName(name):
    book = Book.query.filter_by(name=name).first()
    bookSchema = BookSchema()
    result = bookSchema.dump(book)

    return jsonify(result)


@app.route("/api/books/", methods=["POST"])
def addOneBook():
    newBook = Book(name=request.json["name"], pages=request.json["pages"])
    db.session.add(newBook)
    db.session.commit()

    book_dict = {
        "id": newBook.id,
        "name": newBook.name,
        "pages": newBook.pages
    }

    return jsonify(book_dict)


@app.route("/api/books/<int:id>", methods=["PUT"])
def updateOneBook(id):
    book = Book.query.filter_by(id=id).first()
    book.name = request.json["name"]
    book.pages = request.json["pages"]

    db.session.commit()

    book_dict = dict(id=book.id, name=book.name, pages=book.pages)
    return jsonify(book_dict)


@app.route("/api/books/<int:id>", methods=["DELETE"])
def deleteOneBook(id):
    book = Book.query.get(id)

    db.session.delete(book)
    db.session.commit()

    return jsonify({book.name: "deleted"})


if __name__ == "__main__":
    app.run()
