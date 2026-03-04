from http.server import BaseHTTPRequestHandler
import json

class RestError(Exception): 
    
    def __init__(self, code:int=500, phrase:str="Internal Error", data:any=None): 
        self.code   = code 
        self.phrase = phrase 
        self.data   = data 
  
    def __str__(self): 
        return "RestError(%d, '%s', %r)" % (self.code, self.phrase, self.data)
    
    def __json__(self):
        return { "code": self.code, "phrase": self.phrase, "data": self.data }
    
    def __iter__(self):
        for k,v in self.__json__().items() :
            yield k,v 
  


class ControllerRest :

    def __init__(self, handler:BaseHTTPRequestHandler):
        self.handler = handler


    def serve(self):
        # готуємо self.rest_response
        self.rest_response = {
            "status": {
                "isOk": True,     
                "code": 200,      
                "phrase": "OK"    
            },
            "data": None
        }
        mname = 'do_' + self.handler.command
        if not hasattr(self, mname):
            self.rest_response["status"] = {
                "isOk": False,     
                "code": 405,      
                "phrase": "Unsupported method (%r) for controller (%r)" % 
                            (self.handler.command, self.handler.service)
            }
        else :
            try :    
                method = getattr(self, mname)
                method()
            except RestError as err :
                self.rest_response["status"] = {
                    "isOk": False,     
                    "code": err.code,
                    "phrase": err.phrase
                }
                self.rest_response["data"] = err.data
            except Exception as err :
                self.rest_response["status"] = {
                    "isOk": False,     
                    "code": 500,      
                    "phrase": "Internal Error " + str(err)
                }
        # надсилаємо self.rest_response
        self.handler.send_response(200, "OK")
        self.handler.send_header("Content-Type", "application/json; charset=utf-8")
        self.handler.end_headers()
        self.handler.wfile.write( 
            json.dumps(
                self.rest_response,
                ensure_ascii=False
            ).encode() 
        )
