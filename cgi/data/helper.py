import base64, hashlib, hmac, json, random, string

from models.cgi_request import CgiRequest

def salt(len:int=16) -> str :
    symbols = string.ascii_letters + string.digits
    return "".join( random.choice(symbols) for _ in range(len) )


def hash(input:str) -> str :
    h = hashlib.sha256()
    h.update(input.encode('utf-8'))
    return h.hexdigest()


def kdf(password:str, salt:str) -> str :
    t = hash(password + salt)
    for _ in range(1000) :
        t = hash(t)
    return t[:32]    


def get_signature(data:bytes|str, key:bytes|None=None, alg:str="HS256", enc:str="base64url") -> str :
    if key is None :
        key = b"secret"  # TODO: перенести до змінних оточення або файлу-ініціалізатору

    if isinstance(data, str) :
        data = data.encode()

    if enc == "base64url" :
        match alg :
            case "HS256" :
                hash_alg = hashlib.sha256
            case "HS384" :
                hash_alg = hashlib.sha384
            case "HS512" :
                hash_alg = hashlib.sha512
            case _ :
                raise ValueError("Signature Algorythm not recognized: " + alg)    
        return base64.urlsafe_b64encode( 
            hmac.new(
                key,
                data,
                hash_alg
            ).digest()
        ).decode("ascii")
    else :
        raise ValueError("Encoder not recognized: " + enc)    


def b64u_to_json(input:str) -> any :
    return json.loads( base64.urlsafe_b64decode(input).decode() )


def validate_jwt(jwt:str) -> dict :
    '''
    JWT Validation by RFC 7519 sec.7.2

    raises ValueError if validation failed
    
    :param jwt: JWT token
    :type jwt: str
    :return: JWT payload or None
    :rtype: dict | None
    '''
    if not isinstance( jwt, str ) :
        raise ValueError("Parameter 'jwt' must be of type 'str'")
    parts = jwt.split('.', 1)
    if len(parts) < 2 :
        raise ValueError("JWT must contain at least one period ('.')")
    header = b64u_to_json(parts[0])
    if not isinstance(header, dict) :
        raise ValueError("JWT header must be valid JSON")
    typ = header.get("typ", None)
    if typ != "JWT" :
         raise ValueError("JWT header must contain 'typ' field with value 'JWT'")
    alg = header.get("alg", None)
    if alg is None :
         raise ValueError("JWT header must contain 'alg' field")
    parts2 = parts[1].split('.')
    if len(parts2) != 2 :
        raise ValueError("JWT must contain exactly 3 parts separated by '.'")
    token_body = parts[0] + '.' + parts2[0]
    if get_signature(token_body, alg=alg) != parts2[1] :
        raise ValueError("JWT signature failure")
    payload = b64u_to_json(parts2[0])
    if not isinstance(payload, dict) :
        raise ValueError("JWT payload (Message) must be valid JSON")
    return payload


def authorize_request(req:CgiRequest) -> dict :
    '''
    Extract JWT from request, validate and return JWT payload

    Raise ValueError if authorization fails
    
    :return: JWT payload
    :rtype: dict
    '''
    auth_header = req.headers.get('Authorization', None)
    if auth_header is None :
        raise ValueError("Request must include 'Authorization' header")
    auth_scheme = 'Bearer '
    if not auth_header.startswith(auth_scheme) :
        raise ValueError("Authorization scheme must be " + auth_scheme)
    return validate_jwt( auth_header[len(auth_scheme):] )


def main() :
    try :
        print(validate_jwt('eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJqdGkiOiAiYzhkMGFkYjUtYWFhOS00OGJkLWIzYzEtNjE2Y2M2MWVkNTU2IiwgInN1YiI6ICI2OTIzMWM1NS05ODUxLTExZjAtYjFiNy02MjUxNzYwMDU5NmMiLCAiaWF0IjogMTc2NTI3OTM1NCwgImV4cCI6IDE3NjUyNzk0MTQsICJuYW1lIjogIkRlZmF1bHQgQWRtaW5pc3RyYXRvciIsICJlbWFpbCI6ICJhZG1pbkBsb2NhbGhvc3QifQ==.fIeR5m8SK_2urLp6ZRMYz_pXqmuKT1BZTq7EfjLj9sY='))
    except ValueError as err :
        print(err)


if __name__ == "__main__" :
    main()

'''
Д.З. У складі сторінки "Тестування API: User"
реалізувати інструментарій для перевірки виняткових
ситуацій з JWT
- відсутність заголовку Авторизації
- неправильна схема Авторизації
- у токена відсутній символ "."
- заголовок токена не декодується як В64
- декодований В64 заголовок токена не декодується як рядок (UTF-8)
... (орієнтуємось на порядок перевірки за стандартом https://datatracker.ietf.org/doc/html/rfc7519#section-7.2)
'''