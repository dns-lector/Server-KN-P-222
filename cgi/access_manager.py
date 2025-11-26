#!C:\Python\Python313\python.exe

DEV_MODE = True

import importlib, io, os, sys
from models.cgi_request import CgiRequest

def quit() :
    sys.stdout.flush()                                  # перед "жорстким" перериванням 
    os._exit(0)                                         # необхідно звільнити буфер виведення


request = {k: v  for k,v in os.environ.items() if       # параметри від сервера передаються через змінні оточення,
 k in ('REQUEST_METHOD','QUERY_STRING','REQUEST_URI')}  # які доступні через пакет os

query_params = { k:v for k,v in (
    x.split('=', 1) if '=' in x else (x, None)   
        for x in request['QUERY_STRING'].split('&') ) }

if query_params.get('am-token', None) != '16515318' :
    print("Status: 403 Forbidden\n")                    # перевірка роботи диспетчера доступу
        
    
path = request['REQUEST_URI'].split('?', 1)[0]          # запит без параметрів - усе, що іде до '?'
if not path.endswith('/') and '.' in path :             # перевірка чи є запит на статичний файл
    if '../' in path or '..\\' in path :                # DT-символи -- ознака зловмисних дій
        print("Status: 400 Bad Request\n")
        quit()
    try :               
        ext = path[(path.rindex('.') + 1):]
        media_types = {
            'jpg' : "image/jpeg",
            'jpeg': "image/jpeg",
            'png' : "image/png",
            'bmp' : "image/bmp",
            'css' : "text/css",
            'js'  : "text/javascript",
        }
        if ext in media_types :                         # обмежуємо статичні файли директорією /static
            with open(os.path.abspath('./static/') + path, "rb") as file :
                sys.stdout.buffer.write(f"Content-Type: {media_types[ext]}\n\n".encode())
                sys.stdout.buffer.write(file.read())
            quit()
    except:
        pass

# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())
sys.stdout = io.TextIOWrapper(                          # Змінюємо кодування за замовчанням (cp1251)
    sys.stdout.buffer, "utf-8")                         #  на utf-8
sys.stdin = io.TextIOWrapper( 
    sys.stdin.buffer, "utf-8")       

path_parts = path.split('/', 3)                         # маршрутизація: використаємо ідею як в ASP:
controller = (path_parts[1]                             #   /Controller(Home)/Action(Index)/Id(None)
              if len(path_parts) > 1                    # [0] - завжди порожній,   
              and len(path_parts[1]) > 0                #   оскільки path починається з '/'            
              else 'home')                              # 
sys.path.append("./")                                   # розширюємо місця пошуку імпортованих модулів
try :    
    controller_module = importlib.import_module(        # динамічний імпорт - можливість додавання модулів 
        "controllers.%s_controller" % (                 # під час роботи програми: importlib -       
            controller.lower(),                         #  інструментарій динамічного імпорту
    ))                                                  # намагаємось підключити модуль з класом контролера
    controller_class = getattr(                         # дістаємось класу контролера з підключеного модуля
        controller_module, 
        controller.capitalize() + "Controller")    
    controller_object = controller_class(               # створюємо об'єкт відповідного класу (істантіюємо)
        CgiRequest(                                     # в інтерпретаторах літерали можуть 
            server=request,                             # міститись у змінних
            query=query_params,
            path=path,
            path_parts=path_parts[1:],
            headers={ '-'.join(x.capitalize() for x in k[5:].split('_')):v 
                    for k, v in os.environ.items() if k.startswith('HTTP_') }),
        DEV_MODE
    )    
    controller_action = getattr(                        # знаходимо в об'єкт-контролері метод за назвою 
        controller_object, "service")                   # та виконуємо (викликаємо) його -                    
    controller_action()                                 #  передаємо обробку на контролер     
except Exception as err :
    print("Status: 404 Not Found\n")
    if DEV_MODE :
        print(err)
finally :
    quit()