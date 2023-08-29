# Декоратор, инициализирующий генератор.
def coroutine_init(func):
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        gen.send(None)
        return gen
    return wrapper


class MyException(Exception):
    pass


# Подгенератор.
def sub_gen():
    while True:
        try:
            message = yield
        except MyException:
            print("My exception!")
            break
        except StopIteration:
            break
        else:
            print(message)

    return "Return from sub_gen()"


# Делегатор.
@coroutine_init
def delegator(gen):

    # while True:
    #     try:
    #         data = yield
    #         gen.send(data)
    #     except MyException as e:
    #         gen.throw(e)
    #     except StopIteration as e:
    #         gen.throw(e)

    # Так как код в делегаторе и вызываемом генераторе похожи, то, чтобы не было дублирования, можно воспользоваться
    # конструкцией yield from. Эта конструкция позволяет заменить цикл, проворачивающий подгенератор. Она берёт на себя
    # функцию передачи данных и исключений в подгенератор, а также получает возвращаемое значение.

    # Конструкция yield from называется await. Смысл его заключается в том, что вызывающий код напрямую управляет
    # работой подгенератора. Пока это происходит, делегатор остаётся заблокированным: он вынужден ожидать, когда
    # подгенератор закончит свою работу. Поэтому подгенератор должен содержать в себе механизм, завершающий его работу.

    # yield from уже содержит в себе инициализацию подгенератора, поэтому декоратор у него не нужен.

    # Для чего нужен делегирующий генератор?
    # Делегатор получает то значение, которое возвращает подгенератор с помощью return. Это значение можно
    # дополнительно обработать, и не нужно отлавливать его в StopIteration как в 4_coroutines.py.

    result = yield from gen
    print(result)


print("Delegator:")
sg = sub_gen()
d = delegator(sg)
d.send("My message")
d.send("My message 2")
try:
    d.throw(StopIteration)
except StopIteration:
    pass
print()


# Строго говоря yield from просто отдаёт нам результат из любого итерируемого объекта.
def simple_gen():
    yield from "tim"


print("Example of simple yield from:")
simp_g = simple_gen()
print(next(simp_g))
print(next(simp_g))
print(next(simp_g))
print(next(simp_g))
