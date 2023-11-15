import asyncio
import aiohttp


class AsyncSession:
    """Класс, реализующий протокол асинхронного контекстного менеджера."""
    def __init__(self, url):
        self.url = url

    async def __aenter__(self):
        """Магический метод для инициализации асинхронного менеджера контекста."""

        # Класс ClientSession уже реализует протокол контекстного менеджера, и его можно использовать с with.
        # Но в качестве примера реализуем заново.
        self.session = aiohttp.ClientSession()
        response = await self.session.get(self.url)
        return response

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Магический метод для финализации асинхронного менеджера контекста."""
        await self.session.close()


async def check_speed(url):
    """Корутина, вызывающая контекстный менеджер."""
    async with AsyncSession(url) as response:
        # Дожидаемся результата работы корутины .text() у объекта response.
        html = await response.text()
        return f"{url}: {html[:20]}"


async def main():
    res1 = await asyncio.create_task(check_speed("https://facebook.com"))
    res2 = await asyncio.create_task(check_speed("https://youtube.com"))
    res3 = await asyncio.create_task(check_speed("https://google.com"))

    # Сайты выводятся в порядке тормознутости ответа (первый самый быстрый).
    print(res1)
    print(res2)
    print(res3)


class ServerError(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return self._message


async def return_server_err():
    await asyncio.sleep(2)
    raise ServerError("Failed to get data.")


async def main_gather():

    urls = [
        "https://avito.ru",
        # "https://ghsdgsdggsgsdgn.com",
        "https://youtube.com",
        "https://google.com"
    ]

    coroutines = [check_speed(url) for url in urls]

    results = await asyncio.gather(
        *coroutines,
        return_server_err(),
        return_exceptions=True
    )

    for result in results:
        print(result)

    # for coroutine in asyncio.as_completed(coroutines):
    #     result = await coroutine
    #     print(result)

    # group1 = asyncio.gather(
    #     check_speed("https://youtube.ru"),
    #     check_speed("https://google.com")
    # )
    #
    # group2 = asyncio.gather(
    #     check_speed("https://google.com"),
    #     check_speed("https://youtube.com")
    # )
    #
    # groups = asyncio.gather(group1, group2)
    # results = await groups
    #
    # for result in results:
    #     print(result)


# asyncio.run(main())
print()
asyncio.run(main_gather())
