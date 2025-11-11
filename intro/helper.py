import hashlib, random, string

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


def main() :
    print(kdf("123", "456"))


if __name__ == "__main__" :
    main()

# print(__name__)