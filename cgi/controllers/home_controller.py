from models.cgi_request import CgiRequest

class HomeController :

    def __init__(self, cgi_request:CgiRequest, dev_mode:bool=False):
        self.cgi_request = cgi_request
        self.dev_mode = dev_mode


    def service(self) :
        action_name = (self.cgi_request.path_parts[1].lower()             
            if len(self.cgi_request.path_parts) > 1 
                and len(self.cgi_request.path_parts[1]) > 0 
            else 'index')
        try :
            action = getattr(self, action_name)
            action()
        except Exception as err :
            print("Status: 404 Not Found\n")
            if self.dev_mode :
                print(err)


    def privacy(self) :
        html = self._layout().replace(
            "*RenderBody*", '''
            <h1>Політика конфіденційності</h1>
        ''')                              
        print("Content-Type: text/html; charset=utf-8")
        print()
        print(html)
        

    def index(self) :
        envs = "<ul>" + "".join(f"<li>{k} = {v}</li>" for k,v in self.cgi_request.server.items() ) + "</ul>"
        qp   = "<ul>" + "".join(f"<li>{k} = {v}</li>" for k,v in self.cgi_request.query.items()  ) + "</ul>"
        hdrs = "<ul>" + "".join(f"<li>{k} = {v}</li>" for k,v in self.cgi_request.headers.items()) + "</ul>"

        html = self._layout().replace(
            "*RenderBody*", f'''
            <h1>Інтерфейс спільного шлюзу (CGI)</h1>
            <a href="/home/privacy">Політика конфіденційності</a>
            {envs}
            {qp}
            {hdrs}
            <img src="/img/m13.jpg" />''')   
        print("Content-Type: text/html; charset=utf-8")
        print()   # порожній рядок відділяє заголовки та тіло
        print(html)


    def _layout(self) :
        return '''<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CGI-222</title>
            <link rel="icon" href="/img/Python.png" />
            <link rel="stylesheet" href="/css/site.css" />
        </head>
        <body>
            *RenderBody*
            <script src="/js/site.js"></script>
        </body>
        </html>'''
    


'''
Д.З. Реалізувати метод HomeController - params
до якого перенести таблиці з параметрами:
 змінні оточення, заголовки, параметри запиту (query)
стартову сторінку (index) представити у вигляді змісту:
 назва розділу -- посилання на нього
 + додати неправильні посилання 
  а) на неправильний контролер
  б) на неправильний метод існуючого контролера 
'''    