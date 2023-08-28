import requests
from time import time
import asyncio
import aiohttp  # asyncio предоставляет API для работы с UDP/TCP, но не с HTTP, поэтому нужна библиотека.


URL = "https://loremflickr.com/320/240"  # Url сайта с картинками.
NUM_IMAGES = 10
DIR_IMAGES = "images"


# Получение картинки.
def get_file(url):
    resp = requests.get(url, allow_redirects=True)
    return resp


# Запись картинки в файл.
def write_file(response):
    path = f"{DIR_IMAGES}/{response.url.split('/')[-1]}"
    with open(path, "wb") as file:
        file.write(response.content)


async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        write_image(data)


def write_image(data):
    path = f"{DIR_IMAGES}/file-{int(time() * 1000)}.jpeg"
    with open(path, "wb") as file:
        file.write(data)


def main_sync():
    t_start = time()

    for _ in range(NUM_IMAGES):
        write_file(get_file(URL))

    print(f"Sync total time: {round(time() - t_start, 3)} sec.")


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
