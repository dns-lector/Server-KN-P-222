from models.cgi_request import CgiRequest
import json, sys

class RestStatus :
    def __init__(self, isOk:bool=True, code:int=200, phrase:str="OK"):
        self.isOk = isOk
        self.code = code
        self.phrase = phrase

    #def __str__(self):
    #    return json.dumps(self.__dict__, ensure_ascii=False)
    
    def __json__(self):
        return {
            "isOk": self.isOk,
            "code": self.code,
            "phrase": self.phrase,
        }
    
RestStatus.status200 = RestStatus(True,  200, "OK")
RestStatus.status401 = RestStatus(False, 401, "UnAuthorized")
RestStatus.status402 = RestStatus(False, 402, "Payment Required")
RestStatus.status403 = RestStatus(False, 403, "Forbidden")
RestStatus.status404 = RestStatus(False, 404, "Not Found")
RestStatus.status405 = RestStatus(False, 405, "Method Not Allowed")



class RestMeta :
    def __init__(self, 
                 serviceName:str="Server-222 API. ",
                 cache:int=0,
                 pagination:dict|None=None):
        self.serviceName = serviceName
        self.cache = cache
        self.pagination = pagination

    #def __str__(self):
    #    return json.dumps(self.__dict__, ensure_ascii=False, allow_nan=False)
    
    def __json__(self):
        return {
            "serviceName": self.serviceName,
            "cache": self.cache,
            "pagination": self.pagination,
        }


class RestResponse :
    def __init__(self, 
                 status:RestStatus=RestStatus.status200, 
                 meta:RestMeta=RestMeta(), 
                 data:any=None):
        self.status = status
        self.meta   = meta
        self.data   = data

    #def __str__(self):
    #    return json.dumps(self.__dict__, ensure_ascii=False)
    
    def __json__(self):
        return {
            "status": self.status,
            "meta": self.meta,
            "data": self.data,
        }
    


class RestController :

    def __init__(self, cgi_request:CgiRequest, dev_mode:bool=False):
        self.cgi_request = cgi_request
        self.dev_mode = dev_mode
        self.rest_response = RestResponse()


    def service(self) :
        action_name = "do_" + self.cgi_request.method.lower()
        try :
            action = getattr(self, action_name)
            self.rest_response.data = action()
        except Exception as err :
            self.rest_response.status = RestStatus.status405
            if self.dev_mode :
                self.rest_response.data = str(err)
            else :
                self.rest_response.data = "API does not support method " + self.cgi_request.method
        finally :
            sys.stdout.buffer.write(b"Content-Type: application/json; charset=utf-8\n\n")
            sys.stdout.buffer.write( 
                json
                .dumps(
                    self.rest_response, 
                    ensure_ascii=False, 
                    default=lambda o: o.__json__() if hasattr(o, '__json__') else str)
                .encode("utf-8") 
            )

