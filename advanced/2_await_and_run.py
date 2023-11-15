import asyncio


async def cor():
    print("first call cor()")
    # Дошли до await, значит python переходит к следующей задаче в событийном цикле - main().
    await asyncio.sleep(1)
    print("second call cor()")
    await asyncio.sleep(1)
    print("third call cor()")


async def main():
    # Метод .all_tasks() возвращает все задачи в событийном цикле.
    print(f"Tasks count: {len(asyncio.all_tasks())}")

    print("main() start working")

    asyncio.create_task(cor())
    print(f"Tasks count: {len(asyncio.all_tasks())}")

    # Как только python доходит до ключевого слова await, вызывающего другую корутину, выполнение которой занимает
    # время, то он переключается на выполнение другой задачи в событийном цикле - cor().
    await asyncio.sleep(1)

    # После того как управление вернулось обратно в main(), в консоль вывелось сообщение.
    # Если на этот момент в событийном цикле есть задачи, то они будут выполняться до следующих в них await.
    # Затем результат вернётся в функцию .run(), которая тут же закроет событийный цикл, даже если какие-то задачи не
    # успели полностью выполниться.
    print("main() end working")

# На этом этапе в событийном цикле лишь одна задача main().
asyncio.run(main())

# Если в main() вызвать .sleep() с задержкой в 1 секунду, то выведется:

# main() start working
# first call cor()
# main() end working
# second call cor()

# Если в main() вызвать .sleep() с задержкой в 0.5 секунды, то выведется:

# main() start working
# first call cor()
# main() end working

# Если в main() вызвать .sleep() с задержкой в 3 секунды, то выведется:

# main() start working
# first call cor()
# second call cor()
# third call cor()
# main() end working
