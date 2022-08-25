from flask import Flask
from flask import request
import sqlite3

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/quotes")
def get_quotes():
    select_quotes = "SELECT * from quotes"
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    cursor.execute(select_quotes)
    quotes = cursor.fetchall()
    print(f"{quotes=}")
    cursor.close()
    connection.close()
    return quotes


# /quotes/1
# /quotes/2
@app.route("/quotes/<int:quote_id>")
# @app.post("/quotes")
def get_quote_by_id(quote_id):
    for quote in quotes:
        if quote["id"] == quote_id:
            return quote
    return f"Quote with id={quote_id} not found", 404


@app.route("/quotes", methods=['POST'])
# @app.post("/quotes")
def create_quote():
    new_quote = request.json
    last_id = quotes[-1]['id']
    new_quote["id"] = last_id + 1
    quotes.append(new_quote)
    return new_quote, 201


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