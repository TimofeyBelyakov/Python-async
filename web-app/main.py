import socket
from views import *


# В Django и Flask используется подобная сущность.
# В Django - список URL_PATTERNS, где каждый элемент - это объект url или path.
# Эти объекты принимают первым аргументом url, а вторым функцию view, которая обрабатывает запрос по этой url.
# Пример: path("/index", index)
URLS = {
    "/": index,
    "/blog": blog
}


# Парсинг запроса клиента: получение метода запроса и url.
def parse_request(request):
    parsed = request.split(" ")
    method = parsed[0]
    url = parsed[1]
    return method, url


# Генерация заголовка ответа.
def generate_headers(method, url):
    if method != "GET":
        return "HTTP/1.1 405 Method not allowed\n\n", 405

    if url not in URLS:
        return "HTTP/1.1 404 Not found\n\n", 404

    return "HTTP/1.1 200 OK\n\n", 200


# Генерация тела ответа.
def generate_content(code, url):
    if code == 404:
        return "<h1>404<p>Not found</p></h1>"

    if code == 405:
        return "<h1>405<p>Method not allowed</p></h1>"

    return URLS[url]()


# Генерация ответа клиенту.
def generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, url)

    return f"{headers + body}".encode()


def run():
    # Сервер (тот, кто принимает запрос).
    # socket.AF_INET - протокол IP v4, socket.SOCK_STREAM - протокол TCP.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Установка параметров для сокета.
    # socket.SOL_SOCKET - уровень установки параметров, в данном случае для нашего сокета,
    # socket.SO_REUSEADDR - допустить повторное использование адреса,
    # третьим аргументом включаем socket.SO_REUSEADDR в True.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Необходимо связать субъект сервера с конкретным адресом и портом.
    # Теперь сокет должен ждать обращения по этому адресу и порту.
    server_socket.bind(("localhost", 5000))

    # Сервер начинает прослушивать адрес с портом.
    server_socket.listen()

    # Поскольку мы не знаем, сколько будет длиться соединение (взаимодействие) с клиентом,
    # то используем бесконечный цикл.
    while True:
        # Когда сервер что-то принял от клиента. Возвращает сокет и адрес клиента.
        client_socket, addr = server_socket.accept()

        # Сам запрос от клиента. Принимает кол-во байт в пакете, возвращает запрос в bytes.
        request = client_socket.recv(1024)
        print(request)
        print(addr)

        # Ответ клиенту.
        response = generate_response(request.decode("utf-8"))

        # Отправка ответа клиенту.
        client_socket.sendall(response)

        # Закрытие соединения.
        client_socket.close()


if __name__ == "__main__":
    run()
