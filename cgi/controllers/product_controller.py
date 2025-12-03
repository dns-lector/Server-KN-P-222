import json, sys
from controllers.controller_rest import RestController, RestStatus

class ProductController(RestController) :

    def do_get(self) :
        # Визначити чи є у запиті заголовок авторизації за схемою Bearer
        auth_header = self.cgi_request.headers.get('Authorization', '')
        has_bearer = auth_header.startswith('Bearer ')
        bearer_token = auth_header[7:] if has_bearer else None
        jwt_parts = dict( 
            zip( 
                ("header", "payload", "signature"), 
                bearer_token.split('.') 
            ) 
        ) if has_bearer else None

        test_data = {
            "auth": "Bearer" if has_bearer else "No or not Bearer",
            "method": self.cgi_request.method,
            "token": jwt_parts
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