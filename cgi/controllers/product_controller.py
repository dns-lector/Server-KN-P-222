import json, sys
from controllers.controller_rest import RestController, RestStatus
from data.helper import * 

class ProductController(RestController) :

    def do_get(self) :
        try :
            payload = authorize_request(self.cgi_request)
        except ValueError as err :
            validation_error = str(err)
            payload = None
        else :
            validation_error = None

        test_data = {
            "payload": payload,
            "error": validation_error
        }
        return test_data
    

    def do_post(self) :
        test_data = {
            "cyrr": "Вітання усім!",
            "body": json.load(sys.stdin),
            "method": self.cgi_request.method,
            "headers": self.cgi_request.headers
        }
        return test_data

'''
Д.З. Перевести OrderController (з попередніх ДЗ) до спадкування RestController
Додати до його методів засоби визначення заголовку авторизації та схеми Bearer
Реалізувати відмову в обслуговуванні запитів за умови відсутності зазначеної авторизації
'''