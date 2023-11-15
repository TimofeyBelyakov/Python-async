from inspect import iscoroutinefunction
import asyncio


# Генераторная функция.
def gen_func():
    yield "Generator result\n"


# Корутинная функция.
async def cor_func():
    return "Coroutine result\n"


print(type(gen_func))

# Когда вызывается генераторная функция, то она возвращает объект генератора.
gen = gen_func()
print(type(gen), "\n")

print(type(cor_func))
print(iscoroutinefunction(cor_func))

# Когда вызывается корутинная функция, то она возвращает объект корутину, но не выполняется.
cor = cor_func()
print(type(cor))
print(iscoroutinefunction(cor), "\n")

# Корутины выполняются только в событийных циклах. Событийный цикл реализуется с помощью метода .run().
# Функция .run() запускает событийный цикл в текущем потоке. В потоке может быть только один событийный цикл.
res = asyncio.run(cor)
print(res)


async def sleep():
    print("Wait 2 seconds!")
    # await используется для вызова других корутин.
    # await всегда принимает аргумент: либо другой объект корутины, либо awaitable объекты.
    # await можно использовать только внутри корутиновых функций.
    # await приостанавливает выполнение той корутины, в которой она прописана.
    await asyncio.sleep(2)  # корутина
    print("End sleeping", "\n")


asyncio.run(sleep())


async def one():
    return "Func 1"


async def two():
    await asyncio.sleep(2)
    return "Func 2"


async def main():
    print("Wait 2 seconds!")
    # Такая реализация даёт абсолютно синхронное поведение, так как результат выведется только после выполнения всех
    # корутин. Хочется, чтобы сначала сразу вывелся результат для one(), а через некоторое время для two().
    res1 = await one()
    res2 = await two()  # ставит на паузу main().
    print(res1)
    print(res2)


asyncio.run(main())
