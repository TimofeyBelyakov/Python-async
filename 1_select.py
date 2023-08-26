import socket
from select import select


# Список, содержащий файловые объекты (сокеты) для мониторинга
to_monitor = []


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("localhost", 5001))
server_socket.listen()


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print(f"Connection from: {addr}")

    # Добавление клиентского сокета в очередь для мониторинга
    to_monitor.append(client_socket)


def send_message(client_socket):
    try:
        request = client_socket.recv(4096)
    except ConnectionResetError:
        request = None

    if request is not None:
        response = "Hello world!\n".encode()
        client_socket.send(response)
    else:
        client_socket.close()


def event_loop():
    while True:
        # Select получает три списка, объекты которых нужно мониторить.
        # 1 список - объекты, за которыми надо наблюдать, когда они станут доступны для чтения.
        # 2 список - когда они станут доступны для записи.
        # 3 список - объекты, в которых могут появиться ошибки.
        # Возвращает те же самые объекты после того, как они станут доступны.
        ready_to_read, _, _ = select(to_monitor, [], [])  # read, write, errors

        # Проходимся по всем сокетам, готовым для чтения
        for socket in ready_to_read:
            # Если сокет серверный, то ждём соединения
            if socket is server_socket:
                accept_connection(socket)
            # Если сокет клиентский, то отправляем ответ
            else:
                send_message(socket)


if __name__ == "__main__":
    # Добавление серверного сокета в очередь для мониторинга
    to_monitor.append(server_socket)
    # Запуск событийного цикла
    event_loop()
