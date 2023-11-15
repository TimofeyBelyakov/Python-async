import asyncio
import aiohttp


class WriteToFile:
    """Класс, реализующий протокол синхронного контекстного менеджера."""
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        """Магический метод для инициализации менеджера контекста."""
        self.file_object = open(self.filename, "w")
        # Результат работы метода будет доступен в части as.
        return self.file_object

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Магический метод для финализации менеджера контекста."""
        if self.file_object:
            self.file_object.close()


with WriteToFile("3_test.txt") as file:
    file.write("Hello")


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
        print(f"{url}: {html[:20]}")


async def main():
    res1 = asyncio.create_task(check_speed("https://facebook.com"))
    res2 = asyncio.create_task(check_speed("https://youtube.com"))
    res3 = asyncio.create_task(check_speed("https://google.com"))

    # Сайты выводятся в порядке тормознутости ответа (первый самый быстрый).
    await res1
    await res2
    await res3


asyncio.run(main())
