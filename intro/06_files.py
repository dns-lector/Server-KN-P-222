# Робота з файлами
def write_file(filename:str="file.txt") -> None :
    'Приклад без ресурсного блоку - звільнення ресурсу забезпечує код'
    file = None
    try :
        file = open(filename, mode="w", encoding='utf-8')
        file.write("Latin data\n")    # новий рядок не переводиться, символ потрібний у даних
        file.write("Кириличні дані")  # перевірка того, що необхідно зазначати encoding
        file.flush()
    except OSError as err :
        print("File write error:", err)
    else :
        print("File write Ok")
    finally:
        if file != None :
            file.close()


def write_file2(filename:str="file2.txt") -> None :
    'Приклад з ресурсним блоком - звільнення ресурсу автоматичне'
    try:
        with open(filename, mode="w", encoding='utf-8') as file :
            file.write("Latin data\n")  
            file.write("Кириличні дані")
    except OSError as err :
        print("File write error:", err)
    else :
        print("File write Ok")


def read_file(filename:str="file.txt") -> None :
    try:
        with open(filename, encoding='utf-8') as file :
            # print(file.read())  # зчитує весь контент файлу як рядок
            for line in file :    # ітерація файлу іде по рядках (\n)
                print(line)       # сам символ '\n' залишається у рядку
                print('---')
    except OSError as err :
        print("File read error:", err)
    else :
        print("-----File read end-----")


def read_ini(filename:str="db.ini") -> dict :
    '''Відкриває файл конфігурації типу "ini", 
    ігнорує коментарі, повертає словник за принципом "ключ": "значення".
    OSError передається від файлової роботи.
    Імперативний стиль програмування'''
    res = {}
    with open(filename, encoding='utf-8') as file :
        for line in file :
            if line.startswith('#') :
                continue
            line = line.split('#')[0]  # залишаємо лише те, що передує символу коментаря
            if not ':' in line :       # перевіряємо чи правильний це запис
                continue
            pair = line.split(':', 1)  # !! 1 - кількість ділень (на противагу C#/Java де зазначається розмірність)
            res[pair[0].strip()] = pair[1].strip()  # ~trim()   # [:-1]   # slice [start:end:step]
    return res



def read_ini2(filename:str="db.ini") -> dict :
    'Функціональний стиль'
    with open(filename, encoding='utf-8') as file :
        return { k: v  for k,v in (
            map( str.strip, line.split('#')[0].split(':', 1) ) 
                for line in file if ':' in line
        ) }


def main() :
    try :
        print(read_ini())
        print(read_ini2())
    except OSError as err :
        print(err)


if __name__ == '__main__':
    main()

'''
Модифікувати парсер ini-файла з урахуванням того,
що коментарі можуть бути задані як символом "#", так і ";"
Додавати скріншот роботи програми
'''