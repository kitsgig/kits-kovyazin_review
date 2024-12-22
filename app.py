from database import create_database_and_table
from flask import Flask, render_template, request
import sqlite3
from parsing import parsing

app = Flask(__name__)


def get_cars(year=None, body_color=None, int_color=None, body=None, cnt_place=None, have=None):
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()

    query = "SELECT * FROM cars WHERE 1=1"
    params = []

    if year:
        if '-' in year:
            start_year, end_year = map(int, year.split('-'))
            query += " AND years BETWEEN ? AND ?"
            params.extend([start_year, end_year])
        else:
            query += " AND years = ?"
            params.append(year)

    if body_color:
        query += " AND body_color = ?"
        params.append(body_color)

    if int_color:
        query += " AND int_color = ?"
        params.append(int_color)

    if body:
        query += " AND body = ?"
        params.append(body)

    if cnt_place:
        query += " AND cnt_place = ?"
        params.append(cnt_place)

    if have:
        query += " AND have LIKE ?"
        params.append(have + "%")

    cursor.execute(query, params)
    cars = cursor.fetchall()
    conn.close()
    return cars


@app.route('/', methods=['GET'])
def index():
    year = request.args.get('year')
    body_color = request.args.get('body_color')
    int_color = request.args.get('int_color')
    body = request.args.get('body')
    cnt_place = request.args.get('cnt_place')
    have = request.args.get('have')

    cars = get_cars(year, body_color, int_color, body, cnt_place, have)

    return render_template('index.html', cars=cars)


if __name__ == '__main__':
    create_database_and_table()
    app.run(debug=False, host="0.0.0.0", port=5000)
