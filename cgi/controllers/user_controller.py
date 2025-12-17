from controllers.controller_rest import RestController, RestStatus
import datetime, json, sys, time
from data.accessor import DataAccessor
import data.helper as helper


class UserController(RestController) :

    def __init__(self, cgi_request, dev_mode = False):
        super().__init__(cgi_request, dev_mode)
        self.rest_response.meta.serviceName += "User"


    def do_get(self) :
        # перевіряємо автентифікацію
        try :
            (login, password) = helper.authenticate_request(self.cgi_request)
        except ValueError as err :
            self.rest_response.status = RestStatus.status401
            return str(err)
        data_accessor = DataAccessor()
        user = data_accessor.authenticate(login, password)
        if user is None :
            self.rest_response.status = RestStatus.status401
            return "Credentials rejected"
        # генеруємо токен:
        token = helper.compose_jwt(              # Д.З. Реалізувати метод helper.jwt_for_user(user)
            sub=user['user_id'],                 # який візьме на себе формалізм роботи з утворення
            claims={                             # JWT за об'єктом БД 'user'
                'name': user['user_name'],       # Внести зміни до контролера, перевірити роботу
                'email': user['user_email'],     # 
            }                                    # 
            #,iat=int(time.time() + 100500)
            #, exp=None, 
            # nbf = int(time.time() + 100500)
        )
        # Якщо є потреба зареєструвати токен, то слід передати його до data_accessor
        return token
        

    def do_post(self) :
        test_data = {
            "cyrr": "Вітання усім!",
            "body": json.load(sys.stdin),
            "headers": self.cgi_request.headers
        }
        return test_data
    

    def do_test(self):
        test = self.cgi_request.query.get("test")
        if test == 'nbf' :
            return helper.compose_jwt(           
                sub='test-iser-id',              
                claims={                          
                    'name': 'test-iser-name',    
                    'email': 'test-iser-id-email',  
                },
                nbf = int(time.time() + 100500)
            )
        elif test == 'exp' :
            return helper.compose_jwt(           
                sub='test-iser-id',              
                claims={                          
                    'name': 'test-iser-name',    
                    'email': 'test-iser-id-email',  
                },
                exp = int(time.time() - 100)
            )
        return "Unrecognized"
             


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