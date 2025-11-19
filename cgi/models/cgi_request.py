# Клас, що збирає до себе усі дані, зібрані диспетчером доступу
class CgiRequest :

    def __init__(self, 
                 server:dict, 
                 headers:dict, 
                 path_parts:list[str], 
                 query:dict, 
                 path:str):
        self.server = server
        self.headers = headers
        self.path_parts = path_parts
        self.query = query
        self.path = path
        self.method = server['REQUEST_METHOD']
