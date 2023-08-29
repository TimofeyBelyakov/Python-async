import requests
from time import time
import os
import asyncio
import aiohttp  # asyncio предоставляет API для работы с UDP/TCP, но не с HTTP, поэтому нужна библиотека.


URL = "https://loremflickr.com/320/240"  # Url сайта с картинками.
NUM_IMAGES = 10
DIR_IMAGES = "images"

if not os.path.exists(DIR_IMAGES):
    os.mkdir(DIR_IMAGES)


# Запись картинки в файл.
def write_image(data, filename):
    with open(f"{DIR_IMAGES}/{filename}", "wb") as file:
        file.write(data)


# Получение картинки.
def get_response(url):
    return requests.get(url, allow_redirects=True)


def main_sync():
    t_start = time()

    for _ in range(NUM_IMAGES):
        response = get_response(URL)
        write_image(response.content, response.url.split('/')[-1])

    print(f"Sync total time: {round(time() - t_start, 3)} sec.")


async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        # Является синхронной функцией, что не очень хорошо, так как блокируется выполнение всего кода.
        # В корутинах вызов синхронных функций крайне не рекомендуется.
        write_image(data, f"file-{int(time() * 1000)}.jpeg")


async def main_async():
    t_start = time()
    tasks = []

    async with aiohttp.ClientSession() as session:
        for _ in range(NUM_IMAGES):
            task = asyncio.create_task(fetch_content(URL, session))
            tasks.append(task)

        await asyncio.gather(*tasks)

    print(f"Async total time: {round(time() - t_start, 3)} sec.")


if __name__ == "__main__":
    main_sync()
    asyncio.run(main_async())
