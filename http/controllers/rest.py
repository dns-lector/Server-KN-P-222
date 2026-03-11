from http.server import BaseHTTPRequestHandler

from urllib.parse import unquote_plus

class RestStatus :
    def __init__(self, is_ok:bool=True, code:int=200, phrase:str="OK"):
        self.is_ok  = is_ok
        self.code   = code
        self.phrase = phrase

    def __json__(self) :
        return {
            "isOk": self.is_ok,
            "code": self.code,
            "phrase": self.phrase,
        }
RestStatus.bad_request_400 = RestStatus(is_ok=False, code=400, phrase="Bad Request")
RestStatus.not_found_404 = RestStatus(is_ok=False, code=404, phrase="Not Found")
RestStatus.internal_500 = RestStatus(is_ok=False, code=500, phrase="Internal Server Error")
'''
Створити статичні поля RestStatus під стандартні коди HTTP статусів (з описами)
'''


class RestError(Exception): 
    
    def __init__(self, code:int=500, phrase:str="Internal Error", data:any=None, status:RestStatus|None=None): 
        self.code   = code 
        self.phrase = phrase 
        self.data   = data 
        self.status = status 
  
    def __str__(self): 
        return "RestError(%d, '%s', %r)" % (self.code, self.phrase, self.data)
    
    def __json__(self):
        return { "code": self.code, "phrase": self.phrase, "data": self.data }
    
    def __iter__(self):
        for k,v in self.__json__().items() :
            yield k,v 
  

class PaginationLinks :
    def __init__(self, first_url:str, last_url:str, prev_url:str|None=None, next_url:str|None=None):
        self.first_url = first_url
        self.prev_url  = prev_url
        self.next_url  = next_url
        self.last_url  = last_url
        
    def __json__(self):
        return { "firstUrl": self.first_url, "prevUrl": self.prev_url, "nextUrl": self.next_url, "lastUrl": self.last_url }


class PaginationMeta :
    def __init__(self, total_items:int, per_page:int, total_pages:int, page:int, links:PaginationLinks):
        self.total_items = total_items
        self.per_page = per_page
        self.total_pages = total_pages
        self.page = page
        self.links = links

    def __json__(self):
        return {
            "totalItems": self.total_items,
            "perPage": self.per_page,
            "totalPages": self.total_pages,
            "page": self.page,
            "links": self.links
        }



class RestMeta :
    def __init__(self, service:str, service_url:str, pagination:PaginationMeta|None=None):
        self.service = service
        self.service_url = service_url
        self.pagination = pagination

    def __json__(self) :
        return {
            "service": self.service,
            "serviceUrl": self.service_url,
            "pagination": self.pagination,
        }
 


class RestResponse :
    def __init__(self, status:RestStatus|None=None, meta:RestMeta|None=None, data:any=None):
        self.status = status if status != None else RestStatus()
        self.meta = meta
        self.data = data

    def __json__(self) :
        return {
            "status": self.status,
            "meta": self.meta,
            "data": self.data,
        }



class ControllerRest :

    def __init__(self, handler:BaseHTTPRequestHandler):
        self.handler = handler
        query_params = {}
        if handler.query_string != None:
            for key, value in (map(lambda x : None if x is None else unquote_plus(x) , 
                                   item.split('=', 1) if '=' in item else [item, None] )
                for item in handler.query_string.split('&') if len(item) > 0) :
                    query_params[key] = value if not key in query_params else [
                        *(  query_params[key] if isinstance(query_params[key], (list,tuple)) 
                            else [query_params[key]] ), 
                        value
                    ]
        self.query_params = query_params
        self.rest_response = RestResponse()


    def serve(self):
        mname = 'do_' + self.handler.command
        if not hasattr(self, mname):
            self.rest_response.status = RestStatus(
                is_ok  = False,     
                code   = 405,      
                phrase = "Unsupported method (%r) for controller (%r)" % 
                            (self.handler.command, self.handler.service)
            )
        else :
            try :    
                method = getattr(self, mname)
                method()
                self.on_success()
                return
            except RestError as err :
                self.rest_response.status = RestStatus(
                    is_ok  = False,     
                    code   = err.code,
                    phrase = err.phrase
                ) if err.status == None else err.status
                self.rest_response.data = err.data
            except Exception as err :
                self.rest_response.status = RestStatus(
                    is_ok  = False,     
                    code   = 500,      
                    phrase = "Internal Error " + str(err)
                )
        self.on_error()

                
    def on_success(self) :
        self.handler.send_rest(self.rest_response)


    def on_error(self) :
        self.handler.send_rest(self.rest_response)



'''
Д.З. Додати до відповіді сервісу /product
реальну вибірку товарів згідно з даними про пагінацію
'''