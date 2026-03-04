from controllers.rest import ControllerRest, RestError


class UserController(ControllerRest) :    

    def do_GET(self) :
        # Зводимо роботу методу до заповнення self.rest_response["data"]
        self.rest_response["data"] = {"GET": "Вітання!"}


    def do_LINK(self) :
        raise RestError(
            code=400, 
            phrase="LINK raised error",
            data="Помилка спеціально створена для випробування механізму спрощення контролерів"
        )
    

'''
Д.З. Реалізувати передачу даних про роботу access_manager 
у складі відповіді UserController (аналогічно Home тільки у JSON):
Приклад для запиту (адреси) "/user/auth?x=10"
"data": {
    "Full Path": "/user/auth"
    "Controller": "UserController"
    "Query String": "x=10"
    "Query Params": {
      "x": 10
    }
    "Service": "user"
    "Service Param": "auth"
}
'''