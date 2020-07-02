import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
import http.client as httplib

import requests

# Целевые узлы
urls = {
    "https://google.com": "GET",
    "https://go.skillbox.ru/api/v1/users/check_email/": "POST",
    "https://identity.qld.gov.au/login/login.html": "GET",
    "https://xakep.ru": "GET",
    "https://www.nasa.gov": "GET",
    "http://www.ciht.org.hk/access": "GET",
    "https://runa.com": "GET",
}

max_executor = 50
count_message_send = 100
executor = ThreadPoolExecutor(max_executor)
summary = {}
task_count = 0
done_task_count = 0
futures = []


async def send_request(url_type, target_url, it):
    """
    Основная функция отправки запроса.
    @params:
        url_type    - Required  : Тип запроса GET или POST
        target_url  - Required  : Целевой урл
        it          - Required  : Номер запроса
    """
    global done_task_count

    request_func = requests.get
    if url_type == "POST":
        request_func = requests.post

    # Выполняем запрос
    response = await loop.run_in_executor(executor, request_func, target_url)

    print(f"\r{done_task_count}\\{task_count}", end="")
    done_task_count += 1

    # Статус 200 - это скучный статус, его мы пропускаем.
    if response.status_code != 200:
        filter_head = f"{target_url}_{response.status_code}"

        # Ограничения на количество одинаковых запросов
        if filter_head not in summary:
            # Вывод полученной информации
            print(f"\rFound: {target_url} - {response.status_code} on {it}")
            for hi, h in enumerate(response.headers):
                print(f"{h} {response.headers[h]}")
            print()

            summary[filter_head] = (target_url,
                                    response.status_code,
                                    response.headers,
                                    response.text)


# Перебор всех urls
# Для каждой ссылке создаём count_message_send запросов
for _, url in enumerate(urls):
    for i in range(count_message_send):
        futures.append(send_request(urls[url], url, i))
        task_count += 1

loop = asyncio.get_event_loop()
# Запуск coroutine
loop.run_until_complete(asyncio.wait(futures))
loop.close()

print("\rРезультат:")
for s in summary:
    url, status_code, headers, text = summary[s]
    info = httplib.responses[status_code]
    print(f"code: {status_code}, info: {info}, url: {url}")
