#!C:\Python\Python313\python.exe

import codecs, os, sys

# параметри від сервера передаються через змінні оточення,
# які доступні через пакет os
request = {k: v  for k,v in os.environ.items() if k in ('REQUEST_METHOD','QUERY_STRING','REQUEST_URI')}

query_params = { k:v for k,v in (
    x.split('=', 1) if '=' in x else (x, None)   
        for x in request['QUERY_STRING'].split('&')   
) }
# перевірка роботи диспетчера доступу
if query_params.get('am-token', None) != '16515318' :
    print("Status: 403 Forbidden")
    print()
    exit()

# перевірка чи є запит на статичний файл
path = request['REQUEST_URI'].split('?', 1)[0]   # запит без параметрів - усе, що іде до '?'
if not path.endswith('/') :    
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
        if ext in media_types :
            with open(os.path.abspath('.') + path, "rb") as file :
                sys.stdout.buffer.write(f"Content-Type: {media_types[ext]}\n\n".encode())
                sys.stdout.buffer.write(file.read())
                sys.stdout.flush()
            exit()
    except:
        pass

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())

headers = { '-'.join(x.capitalize() for x in k[5:].split('_')):v 
           for k, v in os.environ.items() if k.startswith('HTTP_') }

# маршрутизація: використаємо ідею як в ASP: /Controller(Home)/Action(Index)/Id(None)
path_parts = path.split('/', 3)
# [0] - завжди порожній, оскільки path починається з '/'
controller = path_parts[1] if len(path_parts) > 1 and len(path_parts[1]) > 0 else 'home'
action     = path_parts[2] if len(path_parts) > 2 and len(path_parts[2]) > 0 else 'index'
id         = path_parts[3] if len(path_parts) > 3 and len(path_parts[3]) > 0 else None

controller_filename  = controller.lower() + "_controller"       # home_controller
controller_classname = controller.capitalize() + "Controller"   # HomeController

'''
Д.З. Розробити альтернативну версію маршрутизатора, який працюватиме за 
шаблоном:
/Locale(uk-ua)/Controller(Home)/Action(Index)/Id(None)
Перевірити її роботу на адресах
               Locale  Controller  Action  Id
/              uk-ua,  Home,       Index,  None
/en            en,     Home,       Index,  None
/en-us         en-us,  Home,       Index,  None
/en-us/user    en-us,  User,       Index,  None
і так далі
'''

envs = "<ul>" + "".join(f"<li>{k} = {v}</li>" for k,v in request.items()) + "</ul>"
qp = "<ul>" + "".join(f"<li>{k} = {v}</li>" for k,v in query_params.items()) + "</ul>"
hdrs = "<ul>" + "".join(f"<li>{k} = {v}</li>" for k,v in headers.items()) + "</ul>"

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CGI-222</title>
    <link rel="icon" href="/python.png" />
</head>
<body>
    <h1>Інтерфейс спільного шлюзу (CGI)</h1>
    controller: {controller}<br/>
    controller_filename: {controller_filename}<br/>
    controller_classname: {controller_classname}<br/>
    action: {action}<br/>
    id: {id}<br/>

    {envs}
    {qp}
    {hdrs}
</body>
</html>'''

print("Content-Type: text/html; charset=utf-8")
print()   # порожній рядок відділяє заголовки та тіло
print(html)
# Д.З. Реалізувати виведення інформації про змінні оточення CGI
# у вигляді HTML-таблиці. Забезпечити сортування таблиці за іменами змінних