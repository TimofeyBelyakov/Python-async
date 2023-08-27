import socket
import selectors


# Получение дефолтного селектора для ОС.
selector = selectors.DefaultSelector()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 5001))
    server_socket.listen()

    # Регистрация серверного сокета для мониторинга.
    # Принимает файловый объект, событие, которое нас интересует, и любые связанные с этим объектом данные.
    # Здесь в качестве данных передаётся объект-функция, которую необходимо выполнить при наступлении события.
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print(f"Connection from: {addr}")

    # Регистрация клиентского сокета для мониторинга.
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)


def send_message(client_socket):
    try:
        request = client_socket.recv(4096)
    except ConnectionResetError:
        request = None

    if request is not None:
        response = "Hello world!\n".encode()
        client_socket.send(response)
    else:
        # Перед закрытием сокета, его нужно снять с регистрации.
        selector.unregister(client_socket)
        client_socket.close()


def event_loop():
    while True:

        # Возвращает кортеж из двух элементов на каждый зарегистрированный объект.
        # Key - объект SelectorKey, именованный кортеж, который служит для того, чтобы связать между собой сокет,
        # ожидаемое событие и данные, связанные с этим сокетом. У SelectorKey есть те же поля, которые заполняются при
        # регистрации сокета.
        # Events - битовая маска события.
        events = selector.select()  # (key, events)
        for key, _ in events:
            # Callback - функция, которая передавалась при регистрации сокета.
            callback = key.data
            callback(key.fileobj)


if __name__ == "__main__":
    server()
    # Запуск событийного цикла.
    event_loop()
