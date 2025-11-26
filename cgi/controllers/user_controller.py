from models.cgi_request import CgiRequest
import base64, json, sys
from data.accessor import DataAccessor

status401 = {
    "isOk": False,
    "code": 401,
    "phrase": "UnAuthorized"
}

class UserController :

    def __init__(self, cgi_request:CgiRequest, dev_mode:bool=False):
        self.cgi_request = cgi_request
        self.dev_mode = dev_mode


    def service(self) :
        self.rest_response = {
            "status": {},
            "meta": {},
            "data": None
        }
        action_name = "do_" + self.cgi_request.method.lower()
        try :
            action = getattr(self, action_name)
            self.rest_response['status'] = {
                "isOk": True,
                "code": 200,
                "phrase": "OK"
            }
            self.rest_response['data'] = action()
        except Exception as err :
            # print("Status: 405 Method Not Allowed\n")
            self.rest_response['status'] = {
                "isOk": False,
                "code": 405,
                "phrase": "Method Not Allowed"
            }
            if self.dev_mode :
                self.rest_response['data'] = str(err)
            else :
                self.rest_response['data'] = "API does not support method " + self.cgi_request.method
        finally :
            sys.stdout.buffer.write(b"Content-Type: application/json; charset=utf-8\n\n")
            sys.stdout.buffer.write( 
                json
                .dumps(
                    self.rest_response, 
                    ensure_ascii=False, 
                    default=str)
                .encode("utf-8") 
            )


    def do_get(self) :
        # перевіряємо автентифікацію
        auth_header = self.cgi_request.headers.get('Authorization', None)
        if auth_header :
            scheme = 'Basic '
            if not auth_header.startswith(scheme) :
                self.rest_response['status'] = status401
                return "Invalid 'Authorization' scheme"
            else :
                try : 
                    credentials = base64.b64decode(auth_header[len(scheme):].encode()).decode("utf-8")
                except Exception as err : 
                    self.rest_response['status'] = status401
                    return str(err)
                
                (login, password) = credentials.split(':')
                data_accessor = DataAccessor()
                user = data_accessor.authenticate(login, password)
                if user is None :
                    self.rest_response['status'] = status401
                    return "Credentials rejected"
                else :
                    return user
        else :
            self.rest_response['status'] = status401
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