import socket


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("localhost", 5000))
server_socket.listen()

while True:
    print("Before .accept()")
    # Блокирующая операция. Когда клиент подключится, то программа продолжит своё выполнение.
    client_socket, addr = server_socket.accept()
    print(f"Connection from: {addr}")

    # Поскольку сервер принял подключение клиента, то теперь нужно дождаться от клиента какого-либо запроса.
    while True:
        print("Before .recv()")
        # Блокирующая операция. Когда клиент отправит запрос, программа продолжит своё выполнение.
        try:
            request = client_socket.recv(4096)
        except ConnectionResetError:
            request = None

        if request is None:
            break
        else:
            response = "Hello world!\n".encode()
            # При определённых обстоятельствах метод отправки ответа тоже блокирующая операция.
            # Поскольку буфер отправки был пустой, то мы получали ответ сразу.
            # Как только буфер наполнится, то .sendall() станет блокировать выполнение дальнейшего кода,
            # и мы будем вынуждены ждать, пока кто-нибудь не прочитает данные из буфера и он не очистится,
            # чтобы сокет смог туда что-то записать.
            client_socket.sendall(response)

    print("Outside inner while loop")
    client_socket.close()
