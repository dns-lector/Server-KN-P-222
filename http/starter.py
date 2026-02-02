from http.server import HTTPServer, BaseHTTPRequestHandler

class MainHandler(BaseHTTPRequestHandler) :
    def do_GET(self) :
        # print("Hello, world!") -- потрапляє у консоль, не у відповідь сервера
        # self.path - містить повний шлях, у т.ч. параметри
        parts = self.path.split('?')
        path = parts[0]
        query_string = parts[1] if len(parts) > 1 else None
        # Встановлюємо принцип маршрутизації:
        # /Controller/Action/Id, якщо є ще "/", то вони стають частиною Id
        # наприклад
        # /Shop/Product/ASUS/412 -> Controller-Shop, Action-Product, Id-ASUS/412
        parts = path.split('/', 3)
        controller = parts[1].lower() if len(parts) > 1 and len(parts[1]) > 0 else "home"
        action = parts[2].lower() if len(parts) > 2 and len(parts[2]) > 0  else "index"
        id = parts[3] if len(parts) > 3 and len(parts[3]) > 0  else None

        query_params = {}
        if query_string != None:
            for item in query_string.split('&'):
                if len(item) == 0 :
                    continue
                parts = item.split('=', 1)
                if parts[0] in query_params :   # повторна поява параметра має формувати масив значень
                    arr = []
                    if isinstance(query_params[parts[0]], (list,tuple)) :
                        arr.append(*query_params[parts[0]])
                    else :
                        arr.append(query_params[parts[0]])
                    query_params[parts[0]] = [*arr, 
                        parts[1] if len(parts) > 1 else None
                    ]
                else :
                    query_params[parts[0]] = parts[1] if len(parts) > 1 else None

        self.send_response(200, "OK")
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"""
        <h1>HTTP</h1>
        self.path = <b>{self.path}</b><br/>
        path = <b>{path}</b><br/>
        <hr/>
        controller = <b>{controller}</b><br/>
        action = <b>{action}</b><br/>
        id = <b>{id}</b><br/>
        <hr/>
        query_string = <b>{query_string}</b><br/>
        query_params = <b>{query_params}</b><br/>
        """.encode())



def main() :
    port = 88
    http_server = HTTPServer(
        ('127.0.0.1', port),
        MainHandler
    )
    try :
        print(f"Server starting on port {port}...")
        print(f"http://localhost:{port}")
        http_server.serve_forever()
    except :
        print("Server stopped")


if __name__ == "__main__" :
    main()


'''
Модуль HTTP
Альтернативний (до CGI) підхід до створення серверних застосунків
полягає у використанні "власного" сервера, що стає частиною проєкту.
+ використовується єдина мова програмування
+ спрощуються ліцензійні умови
- частіше за все зменшена швидкість роботи сервера
- дотримання стандартів і протоколів перекладається на розробника

Інструментарій знаходиться у модулі http.server:
HTTPServer - клас управління сервером
BaseHTTPRequestHandler - клас оброблення запитів

Особливості даного підходу (як відмінності від CGI)
- скрипт запускається у звичайний спосіб (через main)
- сервер (слухання) запускається через код, вимагається вільний порт
   для запуску сервера.
- stdout спрямовується на консоль, для формування відповіді
   необхідно передавати дані у спеціальний буфер обробника (wfile)




Д.З. Реалізувати відображення даних, що визначені
з запиту (контролер, дія, параметри запиту тощо)
у вигляді HTML-таблиці
|Назва|Значення|   
Додати скріншот результатів
'''
