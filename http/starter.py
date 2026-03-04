from http.server import HTTPServer, BaseHTTPRequestHandler
import socket, sys, importlib
from urllib.parse import unquote_plus


white_mime = {
    ".html": "text/html",
    ".htm": "text/html",
    ".css": "text/css",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".txt": "text/plain",
    ".pdf": "application/pdf",
    ".zip": "application/zip",  
    ".rar": "application/x-rar-compressed",
    ".mp3": "audio/mpeg",
    ".mp4": "video/mp4",
    ".avi": "video/x-msvideo",
    ".mpeg": "video/mpeg",
    ".webm": "video/webm",
    ".ogg": "audio/ogg",
    ".wav": "audio/wav",
    ".flac": "audio/flac",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
}


class AccessManagerRequestHandler(BaseHTTPRequestHandler):
    def handle_one_request(self):
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return
            if not self.raw_requestline:
                self.close_connection = 1
                return
            if not self.parse_request():
                return
            mname = 'access_manager'
            if not hasattr(self, mname):
                self.send_error(501, "Method not implemented: (%r)" % mname)
                return
            method = getattr(self, mname)
            method()
            self.wfile.flush()
        except socket.timeout as e:
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
            return
        
    
    def access_manager(self):
        mname = 'do_' + self.command
        if not hasattr(self, mname):
            self.send_error(501, "Unsupported method (%r)" % self.command)
            return
        method = getattr(self, mname)
        method()
 


class MainHandler(AccessManagerRequestHandler) :
    def access_manager(self):
         # Відокремлення параметрів запиту        
        parts = self.path.split('?', 1)  # Done: відокремити параметри ДО того, як шукати файл
        path = parts[0]
        self.query_string = parts[1] if len(parts) > 1 else None

        # Логіка віддачі статичних файлів 
        if not path.endswith("/") and not "../" in path:
            try:            
                dot_index = path.rindex(".")
                ext = path[dot_index:].lower()
                mime_type = white_mime[ext]
                fname = "./http/assets" + path
                with open(fname, "rb") as file:
                    print(fname, mime_type)
                    self.send_response(200, "OK")
                    self.send_header("Content-Type", mime_type)
                    self.end_headers()
                    self.wfile.write(file.read()) 
                return
            except Exception as err:
                print(err)

       
        query_params = {}
        if self.query_string != None:
            for key, value in (map(lambda x : None if x is None else unquote_plus(x) , 
                                   item.split('=', 1) if '=' in item else [item, None] )
                for item in self.query_string.split('&') if len(item) > 0) :
                    query_params[key] = value if not key in query_params else [
                        *(  query_params[key] if isinstance(query_params[key], (list,tuple)) 
                            else [query_params[key]] ), 
                        value
                    ]
        self.query_params = query_params

        # API - маршрутизація за контролерами        
        parts = path.split('/', 2)
        self.service = parts[1].lower() if len(parts) > 1 and len(parts[1]) > 0 else "home"
        self.service_param = parts[2] if len(parts) > 2 and len(parts[2]) > 0  else None

        # Done: Врахувати перевірки на те, що точно не може бути іменем контролера ('./http/assets/.well-known/appspecific/com.chrome.devtools.json')
        if '.' in self.service :
            self.send_error(404, "Searching prevented for %s" % self.service)
            return
        
        sys.path.append("./") 
        try :    
            controller_module = importlib.import_module("controllers.%s_controller" % (self.service,))                                                  
            controller_class = getattr(controller_module, self.service.capitalize() + "Controller")    
            controller_object = controller_class(self)
            mname = 'serve'
            if hasattr(controller_object, mname):
                method = getattr(controller_object, mname)
                method()
            else :
                mname = 'do_' + self.command
                if not hasattr(controller_object, mname):
                    self.send_error(405, "Unsupported method (%r) for controller (%r)" % (self.command, self.service))
                    return
                method = getattr(controller_object, mname)
                method()            
        except Exception as err :
            print(err)
            self.send_error(404, "Not Found")
        




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


''' q=it+step%20%D0%B0%D0%BA%D0%B0%D0%B4%D0%B5%D0%BC%D1%96%D1%8F
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

Маршрутизація?
MVC                      API
GET  /user/auth |        GET  /user/auth   різні
POST /user/auth |        POST /user/auth   активності
----------------------------------------------------------
GET  /user/profile       GET  /user/profile
інший                    швидше за все, той самий GET User, тільки з іншим параметром

Д.З. Реалізувати відображення даних, що визначені
з запиту (контролер, дія, параметри запиту тощо)
у вигляді HTML-таблиці
|Назва|Значення|   
Додати скріншот результатів

Д.З. Створити на головній сторінці ряд посилань на цю ж сторінку але з різними параметрами:
/?   [без параметрів]
/?x=10&x=20   [масив параметрів]
/?q=it+step%20%D0%B0%D0%BA%D0%B0%D0%B4%D0%B5%D0%BC%D1%96%D1%8F   [url-кодовані параметри]
...
'''

            # for item in query_string.split('&'):
            #     if len(item) == 0 :
            #         continue
            #     key, value = item.split('=', 1) if '=' in item else [item, None]
            #     query_params[key] = value if not key in query_params else [
            #         *( query_params[key] if isinstance(query_params[key], (list,tuple)) 
            #            else [query_params[key]] ), 
            #         value
            #     ]

        # if query_string != None:
        #     for item in query_string.split('&'):
        #         if len(item) == 0 :
        #             continue
        #         parts = item.split('=', 1)
        #         if parts[0] in query_params :   # повторна поява параметра має формувати масив значень
        #             arr = []
        #             if isinstance(query_params[parts[0]], (list,tuple)) :
        #                 arr.append(*query_params[parts[0]])
        #             else :
        #                 arr.append(query_params[parts[0]])
        #             query_params[parts[0]] = [*arr, 
        #                 parts[1] if len(parts) > 1 else None
        #             ]
        #         else :
        #             query_params[parts[0]] = parts[1] if len(parts) > 1 else None
