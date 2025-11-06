# JSON
import json

# формуємо різні дані різних типів, перевіряємо як вони відтворяться
data1 = '''{
    "x": 10,
    "y": 0.123,
    "w": 1.2e-2,
    "t": true,
    "f": false,
    "n": null,
    "arr": [1, 2, "3"],
    "o": {
        "s": "The String",
        "date":"2025-10-29"
    },
    "b": 12345678901234567890123456789,
    "c": "Вітання усім",
    "p": 0.12345678901234567890123456789
}'''

data2 = '''[
    10, 1.23, "String", {"x": 10}
]'''


def main() :
    j = json.loads(data1)  # loads - load from string
    print(type(j), j)      # <class 'dict'> {'x': 10, 'y': 0.123, 'w': 0.012, 't': True, 'f': False, 'n': None, 'arr': [1, 2, '3'], 'o': {'s': 'The String', 'date': '2025-10-29'}}
    for k in j :
        print(k, ":", j[k], type(j[k]))
        # x : 10 <class 'int'>                             ++ цілі числа приймаються як int
        # y : 0.123 <class 'float'>                        ++ дробові числа приймаються як у формі
        # w : 0.012 <class 'float'>                        ++ з точкою, так і в інженерній формі
        # t : True <class 'bool'>                          ++ логічні дані сприймаються як bool
        # f : False <class 'bool'>                         ++ і перетворюються на True False
        # n : None <class 'NoneType'>                      ++ null перетворюється у None
        # arr : [1, 2, '3'] <class 'list'>
        # o : {'s': 'The String', 'date': '2025-10-29'} <class 'dict'>    
        # b : 12345678901234567890123456789 <class 'int'>  ++ великі числа - без спотворень
        # c : Вітання усім <class 'str'>                   ++ кирилиця (юнікод) - без спотворень
        # p : 0.12345678901234568 <class 'float'>          -- висока точність - округлюється

    j2 = json.loads(data2)
    print(type(j2), j2)        # <class 'list'> [10, 1.23, 'String', {'x': 10}]
    print('-----------------------')
    j_str = json.dumps(j)      # dumps - dump to string - серіалізація об'єкту до рядка
    print(j_str)
    # {"x": 10, "y": 0.123, "w": 0.012,       інженерна форма не зберіглася (0.012 замість 1.2e-2)
    #  "t": true, "f": false, "n": null,      логічні та None типи перетворились до JSON формату
    #  "arr": [1, 2, "3"], "o": {"s": "The String", "date": "2025-10-29"}, 
    #  "b": 12345678901234567890123456789,    unicode дані перетворились на коди
    #  "c": "\u0412\u0456\u0442\u0430\u043d\u043d\u044f \u0443\u0441\u0456\u043c", 
    #  "p": 0.12345678901234568}     
    json.dump(j,                       # (без s - запис у файл) додаткові параметри:
            ensure_ascii=False,        #  дозвіл на Unicode
            fp=open("07_json.json",    #  файл, у який ведеться запис
                    mode="w",          #    ! при дозволеному Юнікоді
                    encoding='utf-8'), #      не забуваємо зазначати encoding
            indent=4)                  #  формування відступів (по 4 пробіли)
     
    print('-----------------------')
    try :
        with open("07_json.json", encoding='utf-8') as file :
            j3 = json.load(fp=file,)   # (без s - читання з файлу)
    except OSError as err:
        print("Помилка читання файлу: ", err)
    except json.decoder.JSONDecodeError as err:
        print("Помилка декодування файлу: ", err)
    else :    
        print(type(j3), j3)


if __name__ == '__main__' :
    main()


'''
JSON - JavaScript Object Notation
Формат збереження/передачі даних за синтаксичними правилами мови JavaScript
Прімітиви          JSON
---------------------------
рядок (string)  "The String"
число (int)        123
число (float)      1.23
boolean          true   false
null               null
--------complex-------------
array             [1,2,"3"]
object            {"x":10, "y":20, "date":"2025-10-29"}

??
Як у Python відображаються несумісні типи: true/True, null/None...

Д.З. Реалізувати журнал-логер, який буде фіксувати момент
часу (з датою) запусків програми та зберігати його у JSON 
файлі.
Після запуску програми вона виводить усі моменти запуску
та додає відомості про поточний момент. 
Рекомендована структура файлу:
{
    "program": "exec logger",
    "execMoments": [
        "2025-10-28 12:41:34",
        "2025-10-29 14:45:31",
    ]
}

Запуск:
> програма запускалась попередньо 2 рази о
"2025-10-28 12:41:34",
"2025-10-29 14:45:31",
((+ до файлу додається ще один момент))
'''