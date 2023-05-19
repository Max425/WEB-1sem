from urllib.parse import parse_qsl


def application(environ, start_response):
    # Получение метода запроса (GET, POST и т.д.)
    method = environ['REQUEST_METHOD']

    # Получение пути запроса
    path = environ['PATH_INFO']

    # Получение параметров GET запроса
    query_string = environ.get('QUERY_STRING', '')
    get_parameters = dict(parse_qsl(query_string))

    # Получение параметров POST запроса (если есть)
    post_parameters = {}
    if method == 'POST':
        content_length = int(environ.get('CONTENT_LENGTH', '0'))
        post_data = environ['wsgi.input'].read(content_length).decode()
        post_parameters = dict(parse_qsl(post_data))

    # Формирование ответа
    response = f"Method: {method}\n"
    response += f"Path: {path}\n"
    response += "GET Parameters:\n"
    response += "\n".join([f"{key}: {value}" for key, value in get_parameters.items()])
    response += "\n\n"
    response += "POST Parameters:\n"
    response += "\n".join([f"{key}: {value}" for key, value in post_parameters.items()])

    # Установка заголовков ответа
    status = '200 OK'
    headers = [('Content-type','text/plain')]

    # Запуск функции start_response для отправки заголовков
    start_response(status, headers)

    # Возвращение тела ответа в виде итерируемого объекта
    return [response.encode('utf-8')]
