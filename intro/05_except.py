# Винятки
def throw() :            # Створення винятку - raise
    raise ValueError     # Частіше вживається термін Error

def throw_msg() :
    raise TypeError("Error message")

def throw_ex() :
    raise Exception

def no_throw() :   # Python не має поняття "порожній блок" {} 
    pass           # для цього вживається оператор pass


def main() :
    try :
        no_throw()
    except ValueError :
        print("ValueError detected")
        return
    except TypeError as err:
        print(err)
    except :
        print("Unknown Error detected")
    else :                             # блок else виконується при успішному завершенні
        print("Else block")            #  блоку try, але за умови відсутності return            
    finally :                          # блок finally виконується у будь-якому
        print("Finally block")         #  разі навіть якщо буде return



if __name__ == '__main__' :
    main()
