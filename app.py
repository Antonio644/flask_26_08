from flask import Flask
from flask import request
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'main.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


class QuoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(32), unique=False)
    text = db.Column(db.String(255), unique=False)
    raiting = db.Column(db.SmallInteger(), unique=False)

    def __init__(self, author, text):
        self.author = author
        self.text = text

    def __repr__(self):
        return f"Quote {self.author} {self.text}"

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "text": self.text,
        }


@app.route("/quotes")
# object --> dict --> JSON
def get_quotes():
    quotes = QuoteModel.query.all()
    quotes_dict = []
    for quote in quotes:
        quotes_dict.append(quote.to_dict())
    return quotes_dict


@app.route("/quotes/<int:id>")
def get_quote_by_id(id):
    quote = QuoteModel.query.get(id)
    if quote:
        return quote.to_dict()
    return f"Quote with id {id} not found.", 404


@app.route("/quotes", methods=['POST'])
def create_quote():
    new_quote = request.json
    # quote = QuoteModel(author=new_quote['author'], text=new_quote['text'])
    quote = QuoteModel(**new_quote)
    db.session.add(quote)
    db.session.commit()
    return quote.to_dict(), 201

if __name__ == "__main__":
    app.run(debug=True)