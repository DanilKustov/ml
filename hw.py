import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import os

url_openphish = 'https://openphish.com/'

# Храним уникальные URL
unique_urls = set()

# Читаем уже существующие строки из файла (если файл существует)
if os.path.exists("test2.csv"):
    existing_data = pd.read_csv("test2.csv", header=None)
    # Добавляем существующие URL в множество
    unique_urls.update(existing_data[0].values)

start_time = datetime.now()
end_time = start_time + timedelta(hours=3)

while True:
    if datetime.now() >= end_time:
        print("Скрипт завершает работу через час.")
        break

    page = requests.get(url_openphish, stream=True, allow_redirects=True, timeout=10, verify=False)
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find('table', class_='pure-table pure-table-striped')
    internal_table = table.find('tbody')

    alive_sites = []
    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y %H:%M:%S")
    date = current_time.split(" ")[0]

    # Используем enumerate для получения индекса строки
    for index, tr in enumerate(internal_table.find_all('tr')):
        row = [td.text.strip() for td in tr.find_all('td')]

        # Выводим номер строки
        print(f"Обрабатывается строка {index + 1}: {row}")

        if row:
            url = row[0]
            target = row[1]
            time_req = date + " " + row[2]

            datetime_object = datetime.strptime(time_req, "%m/%d/%Y %H:%M:%S")
            diff_minutes = (now - datetime_object).total_seconds() / 60 - 180

            # Проверяем условие времени
            if diff_minutes < 16:
                # Проверяем, уникален ли URL
                if url not in unique_urls:
                    alive_sites.append(row)  # Добавляем строку в живые сайты
                    unique_urls.add(url)  # Добавляем URL в множество уникальных

    # Если есть новые уникальные сайты, записываем их в файл
    if alive_sites:
        df = pd.DataFrame(alive_sites)
        df.to_csv("final.csv", mode='a', header=False, index=False)

    time.sleep(300)
