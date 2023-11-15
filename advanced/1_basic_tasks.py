import asyncio
from time import time


async def one():
    return "Func 1"


async def two(timeout):
    await asyncio.sleep(timeout)
    return f"Func 2, timeout={timeout} sec."


async def main():
    print("Wait!")

    t_start = time()

    # Данный код уже будет выполняться асинхронно.
    res1 = asyncio.create_task(one())
    res2 = asyncio.create_task(two(1))
    res3 = asyncio.create_task(two(3))
    res4 = asyncio.create_task(two(4))
    res5 = asyncio.create_task(two(2))

    print(await res1)
    print(await res2)
    print(await res3)
    print(await res4)
    print(await res5)

    # Выполнение всех корутин занимает чуть дольше времени, чем выполнение самой длительной.
    print(f"Async total time: {round(time() - t_start, 3)} sec.\n")

    task = asyncio.create_task(one())
    await task
    # Метод .done() возвращает True, если задача завершилась корректно.
    print(task.done())
    # Метод .cancelled() возвращает True, если задача была отменена.
    print(task.cancelled(), "\n")

    # Способ того, как можно отменить выполнение слишком долгой задачи.
    long_task = asyncio.create_task(two(60))
    seconds = 0
    while not long_task.done():
        if seconds == 3:
            # Метод .cancel() отменяет выполнение задачи и возвращает исключение CancelledError.
            long_task.cancel()
            break
        await asyncio.sleep(1)
        seconds += 1
        print(f"Time passed: {seconds} sec.")

    try:
        # Запуск долгой задачи.
        await long_task
    except asyncio.CancelledError:
        print("Task was cancelled!\n")

    # Задачу можно отменить проще.
    print("Wait 3 seconds!")
    long_task = asyncio.create_task(two(60))
    try:
        # Метод .wait_for() позволяет задать максимальное время выполнения задачи. Если задача была отменена, вызывает
        # исключение TimeoutError.
        _ = await asyncio.wait_for(long_task, timeout=3)
    except asyncio.TimeoutError:
        print("Task was cancelled!\n")

    # Если задача выполняется слишком долго, то можно это перехватить.
    print("Wait 4 seconds!")
    long_task = asyncio.create_task(two(4))
    try:
        # Метод .shield() может вызвать исключение TimeoutError, но при этом не отменит задачу.
        _ = await asyncio.wait_for(asyncio.shield(long_task), timeout=2)
    except asyncio.TimeoutError:
        print("Task was running for 2 seconds!")
        # Продолжение выполнения long_task.
        result = await long_task
        print(result)

asyncio.run(main())
