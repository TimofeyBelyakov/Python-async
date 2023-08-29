import asyncio


# Метод будет выводить числа от 1 до бесконечности с некоторой задержкой.
# Синтаксис версии python <= 3.4.
# Данный декоратор создаёт из функции корутину. Если функция уже является генератором, то вернётся она же.
@asyncio.coroutine
def print_nums():
    num = 1
    while True:
        print(num)
        num += 1
        # Поскольку цифры выводятся слишком быстро, то можно воспользоваться задержкой.
        # Функция sleep из модуля time не подойдёт, так как она остановит выполнение всей программы, включая метод
        # print_time(). Поэтому необходимо вызвать блокирующую функцию .sleep() из asyncio, так как она вернёт контроль
        # выполнения в событийный цикл. Поскольку .sleep() корутина, то используется yield from.
        yield from asyncio.sleep(0.1)


# Метод будет выводить время каждые 3 секунды.
# Синтаксис версии python >= 3.5.
async def print_time():
    count = 0
    while True:
        if count % 3 == 0:
            print(f"{count} seconds have passed")
        count += 1
        await asyncio.sleep(1)


async def main():
    # Оборачиваем корутины в экземпляры класса Task.
    # Передавать нужно не ссылку на генератор, а объект.
    task1 = asyncio.ensure_future(print_nums())  # Синтаксис версии python < 3.6.
    task2 = asyncio.create_task(print_time())  # Синтаксис версии python >= 3.6.

    # Теперь надо дождаться их выполнения.
    await asyncio.gather(task1, task2)


if __name__ == "__main__":

    # Синтаксис версии python < 3.7.
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()

    # Синтаксис версии python >= 3.7.
    asyncio.run(main())
