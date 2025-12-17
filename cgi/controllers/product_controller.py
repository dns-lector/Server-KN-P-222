import json, sys, time
from controllers.controller_rest import RestController, RestAuth
from data.helper import * 

class ProductController(RestController) :

    def do_get(self) :
        try :
            payload = authorize_request(self.cgi_request)
            # Кожне з полів JWT є опціональним, перевіряємо їх наявність
            # та валідність за часом: якщо немає жодного з часових полів,
            # то токен відхиляємо
            iat = payload.get("iat", None)
            exp = payload.get("exp", None)
            nbf = payload.get("nbf", None)
            if not any((iat, exp, nbf)):
                raise ValueError("Invalid token: missing time fields")
            # Перевіряємо за пріоритетністю:
            # 1. nbf - якщо є і у майбутньому, то відхиляємо токен як
            #     такий, що не набув чинності
            t = time.time()
            if nbf and nbf > t:                 
                raise ValueError("Token not active yet (nbf violation)")
            # 2. exp - якщо у минулому, то відхиляємо з втратою чинності
            if exp and exp < t:
                raise ValueError("Token expired " + str(t - exp) + " sec ago")
            # 3. якщо немає ані nbf, ані ехр, то перевіряємо, що іаt знаходиться
            # у минулому
            if not nbf and not exp and iat > t:                 
                raise ValueError("Token issued in the future (iat violation)")
        except ValueError as err :
            validation_error = str(err)
            payload = None
            self.rest_response.meta.auth = RestAuth(False, validation_error)
        else :
            validation_error = None
            self.rest_response.meta.auth = RestAuth(True, payload.get("sub"))


        test_data = {
            "name": "Product",
            "price": 100500
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