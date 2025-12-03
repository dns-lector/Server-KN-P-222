from controllers.controller_rest import RestController, RestStatus
import base64, json, sys
from data.accessor import DataAccessor


class UserController(RestController) :

    def __init__(self, cgi_request, dev_mode = False):
        super().__init__(cgi_request, dev_mode)
        self.rest_response.meta.serviceName += "User"


    def do_get(self) :
        # перевіряємо автентифікацію
        auth_header = self.cgi_request.headers.get('Authorization', None)
        if auth_header :
            scheme = 'Basic '
            if not auth_header.startswith(scheme) :
                self.rest_response.status = RestStatus.status401
                return "Invalid 'Authorization' scheme"
            else :
                try : 
                    credentials = base64.b64decode(auth_header[len(scheme):].encode()).decode("utf-8")
                except Exception as err : 
                    self.rest_response.status = RestStatus.status401
                    return str(err)
                
                (login, password) = credentials.split(':')
                data_accessor = DataAccessor()
                user = data_accessor.authenticate(login, password)
                if user is None :
                    self.rest_response.status = RestStatus.status401
                    return "Credentials rejected"
                else :
                    return user
        else :
            self.rest_response.status = RestStatus.status401
            return "No 'Authorization' header in request"
        

    def do_post(self) :
        test_data = {
            "cyrr": "Вітання усім!",
            "body": json.load(sys.stdin),
            "headers": self.cgi_request.headers
        }
        return test_data


'''
REST
{
    status: ...
    meta: ...
    data: ...
}
Д.З. Реалізувати додаткові кнопки перевірки передачі токену
з неправильними даними автентифікації (неправильний логін/правильний пароль, ...)
Додати скріншоти роботи сторінки
'''