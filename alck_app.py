import sqlite3
from flask import Flask
from flask import request
from flask import g
from pathlib import Path
from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'main.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class QuoteModel(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   author = db.Column(db.String(32), unique=False)
   text = db.Column(db.String(255), unique=False)

   def __init__(self, author, text):
       self.author = author
       self.text  = text

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    db.row_factory = make_dicts
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/quotes")
def get_quotes():
    select_quotes = "SELECT * from quotes"
    cursor = get_db().cursor()
    cursor.execute(select_quotes)
    quotes = cursor.fetchall()
    return quotes


# /quotes/1
# /quotes/2
@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    sql = f"SELECT * FROM quotes WHERE id={quote_id};"
    cursor = get_db().cursor()
    cursor.execute(sql)
    quote = cursor.fetchone()
    if quote is None:
        return f"Quote with id={quote_id} not found", 404
    return quote


@app.route("/quotes", methods=['POST'])
def create_quote():
    quote_data = request.json
    connection = get_db()
    cursor = connection.cursor()
    create_quote = "INSERT INTO quotes (author,text) VALUES (?, ?)"
    cursor.execute(create_quote, tuple(quote_data.values()))
    connection.commit()
    return {}, 201  # TODO: доделать возврать созданной цитаты


@app.route("/quotes/filter")
def get_quotes_by_filter():
    params = request.args
    filter_quotes = [quote for quote in quotes if quote["author"] == params["author"]]
    return filter_quotes, 200


# /quotes/4
@app.route("/quotes/<int:id>", methods=['PUT'])
def edit_quote(id):
    new_data = request.json
    for quote in quotes:
        if quote["id"] == id:
            if new_data.get("author"):
                quote["author"] = new_data["author"]
            if new_data.get("text"):
                quote["text"] = new_data["text"]
            return quote, 200
    return f"Quote with id={id} not found", 404


if __name__ == "__main__":
    app.run(debug=True)