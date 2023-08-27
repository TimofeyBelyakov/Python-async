import socket
from select import select


# Список с задачами (генераторами). Обычно используются другие структуры.
tasks = []
# Словари, в ключах которых сокеты, а в значениях - методы.
to_read = {}
to_write = {}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 5001))
    server_socket.listen()

    while True:

        # Когда сокет готов, то функция server() вернёт метку метода, который нужно вызвать, и сам сокет.
        # Метка указывает, в какой словарь пойдёт сокет.
        # То есть вместо того, чтобы зависнуть в ожидании, генератор отдаёт контроль выполнения.
        # Функция ставится на паузу и продолжит своё выполнение тогда, когда метод .accept() готов будет выполниться
        # без задержек.
        yield "read", server_socket
        client_socket, addr = server_socket.accept()  # read

        print(f"Connection from: {addr}")

        tasks.append(client(client_socket))


def client(client_socket):
    while True:
        try:

            yield "read", client_socket
            request = client_socket.recv(4096)  # read

        except ConnectionResetError:
            request = None

        if request is None:
            break
        else:
            response = "Hello world!\n".encode()

            yield "write", client_socket
            client_socket.send(response)  # write

    client_socket.close()


def event_loop():

    while any([tasks, to_read, to_write]):

        # Данный цикл добавляет в tasks генераторы.
        while not tasks:
            # В функцию select() можно передавать любые итерируемые объекты, которые при проходе в цикле
            # давали бы файловые объекты. Словари при проходе в цикле дают ключи, а здесь в качестве ключей - сокеты.
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            # В tasks попадают генераторы, у которых нужно вызвать next().
            for socket in ready_to_read:
                # Pop возвращает значение по ключу и удаляет элемент из словаря.
                tasks.append(to_read.pop(socket))

            for socket in ready_to_write:
                tasks.append(to_write.pop(socket))

        try:
            # Извлечение генератора.
            task = tasks.pop(0)
            # Получение метки метода и сокета.
            mark, socket = next(task)

            # Наполнение словарей to_read и to_write.
            if mark == "read":
                to_read[socket] = task

            if mark == "write":
                to_write[socket] = task
        except StopIteration:
            print("Done!")


if __name__ == "__main__":
    tasks.append(server())
    event_loop()
