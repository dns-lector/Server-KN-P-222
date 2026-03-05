from controllers.rest import ControllerRest


class HomeController(ControllerRest) :
    
    def on_success(self):
        # Done: створити метод для успішного надсилання даних (HTML / JSON)
        self.handler.send_response(200, "OK")
        self.handler.send_header("Content-Type", "text/html; charset=utf-8")
        self.handler.end_headers()
        self.handler.wfile.write(self.html_content.encode())


    def do_GET(self):
        fname = "./http/assets/home.html"
        with open(fname, "r", encoding="utf-8") as file:
            html_content = file.read()
            
        self.html_content = (html_content
            .replace("{self.handler.path}",          str(self.handler.path))    
            .replace("{self.handler.service_param}", str(self.handler.service_param))    
            .replace("{self.handler.service}",       str(self.handler.service))    
            .replace("{self.handler.query_params}",  str(self.query_params))    
            .replace("{self.handler.query_string}",  str(self.handler.query_string))    
        )


    def do_LINK(self) :
        raise ValueError()
        

'''
Реалізувати відображення на головній сторінці структур REST
 для об'єктів та масивів (як варіант: включити ТХТ файли до складу сторінки)
'''