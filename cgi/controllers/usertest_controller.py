from models.cgi_request import CgiRequest

class UsertestController :

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
    

    def index(self) :
        with open("./views/usertest_index.html", mode="rt", encoding="utf-8" ) as file :
            body = file.read()
        self._return_view(body)


    def _return_view(self, body:str) :
        html = self._layout().replace("*RenderBody*", body)
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
    