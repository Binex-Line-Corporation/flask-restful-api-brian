from application import app
from application import errors
from flask import render_template, request, jsonify
import sqlite3


def dictionary1(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def db_cursor():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dictionary1
    return conn.cursor()


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

    
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    all_books = db_cursor().execute('SELECT * FROM books;').fetchall()
    return jsonify(all_books)


@app.route('/api/v1/resources/books/', methods=['GET'])
def api_filter():
    query_parameters = request.args
    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return errors.page_not_found(404)

    query = query[:-4] + ';'

    results = db_cursor().execute(query, to_filter).fetchall()

    return jsonify(results)