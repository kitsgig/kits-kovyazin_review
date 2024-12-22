import requests
from bs4 import BeautifulSoup
import time
import sqlite3

DB_FILE = 'cars.db'


def clear_table():
    print("Очищаю таблицу cars...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cars")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='cars'")
    conn.commit()
    cursor.close()
    conn.close()


def insert_car_to_db(car_data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cars (title, years, body_color, int_color, body, engine, cnt_place, have, cost, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (car_data['Название'], car_data.get('Год', ''),
          car_data.get('Цвет кузова', ''),
          car_data.get('Цвет салона', ''),
          car_data.get('Кузов', ''),
          car_data.get('Двигатель', ''),
          car_data.get('Количество мест', ''),
          car_data.get('Наличие', ''),
          car_data.get('Стоимость', ''),
          car_data.get('Изображение', '')))

    conn.commit()
    cursor.close()
    conn.close()


def parsing():
    URL = 'https://antiqcar.ru/market'

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    clear_table()
    cars = []
    img_urls = []
    links = []
    for div in soup.select('div[class^="flex-item mix"]'):
        a_tag = div.find('a', href=True)
        if a_tag:
            links.append(a_tag['href'])
        img = div.find('img').get("data-src")
        if img.startswith('/d'):
            img = "https://antiqcar.ru" + img
        img_urls.append(img)
    i = 0
    for link in links:
        url = 'https://antiqcar.ru' + link
        response = requests.get(url)
        html = response.text

        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find("h1")

        if title_tag is None:
            print(f"Название для страницы {url} не найдено.")
            continue

        block = soup.find("div", id="block22")

        label = ["Название"]
        value = [title_tag.get_text(strip=True)]

        if block:
            for sub_block in block.find_all("div", class_="765"):
                left = sub_block.find("div", class_="left")
                right = sub_block.find("div", class_="right")

                if left and right:
                    label.append(left.get_text(strip=True).replace(":", ""))
                    value.append(right.get_text(strip=True))

            car_data = dict(zip(label, value))
            car_data['Изображение'] = img_urls[i]
            cars.append(car_data)
            insert_car_to_db(car_data)
            if i % 5 == 0:
                print("Загружаются данные", i + 1, "из", len(links))
        else:
            print(f"Блок с данными для страницы {url} не найден.")

        time.sleep(1)
        i += 1
