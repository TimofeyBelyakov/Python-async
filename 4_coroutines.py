from inspect import getgeneratorstate


# Декоратор, инициализирующий генератор.
def coroutine_init(func):
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        gen.send(None)
        return gen
    return wrapper


# Простой пример корутины.
def sub_gen():
    x = "Ready to accept message"
    # Если yield находится справа от знака равно, то он выполняет две функции: принимает значение и отдаёт.
    # Выполнение yield происходит "уголком":
    #       сначала:
    #           x = "Ready to accept message"
    #           yield x
    #       затем:
    #           message = yield
    #           print(f"Sub_gen received: {message}")
    # Если убрать переменную x, то yield всё-равно будет неявно возвращать None.
    message = yield x
    print(f"Sub_gen received: {message}")


print("Generator sub_gen():")
gen = sub_gen()
print(f"Generator state: {getgeneratorstate(gen)}")
# Чтобы генератору передать аргумент, его сначала нужно проинициализировать - gen.send(None).
# Вместо gen.send(None) можно использовать next(gen).
print(gen.send(None))
print(f"Generator state: {getgeneratorstate(gen)}")
# После вывода сообщения генератор выбрасывает исключение StopIteration.
try:
    gen.send("Hello world!")
except StopIteration:
    print("StopIteration")
print(f"Generator state: {getgeneratorstate(gen)}")
print()


class MyException(Exception):
    pass


@coroutine_init
def average():
    count, summ, avg = 0, 0, None

    while True:
        try:
            x = yield avg
        # С помощью метода .throw() можно пробрасывать в генератор исключения, которые здесь ловятся.
        except StopIteration:
            print("Done!")
            break
        # Можно пробрасывать и собственные исключения.
        except MyException:
            print("My exception!")
            break
        else:
            count += 1
            summ += x
            avg = round(summ / count, 2)

    # Генераторы могут возвращать значение с помощью return.
    return avg


print("Generator average():")
gen = average()
# При каждом вызове .send() возвращается накапливаемое среднее.
print(gen.send(5))
print(gen.send(4))
print(gen.send(10))
# Значение, возвращаемое return, можно перехватить только в обработке исключения StopIteration.
try:
    gen.throw(MyException)
except StopIteration as e:
    print(f"Total average: {e.value}")
