# ORM - використання об'єктного представлення даних
# задача - одержати дані про курси валют з АРІ банку,
# представити їх у вигляді об'єктів

# надсилання запитів: модуль requests
import requests   # pip install requests

url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"

class NbuRate :
    '''{
    "r030": 12,
    "txt": "Алжирський динар",
    "rate": 0.3236,
    "cc": "DZD",
    "exchangedate": "30.10.2025"
  },'''
    def __init__(self, j:dict|None = None):
        self.r030          = j["r030"] if j else None
        self.full_name     = j["txt"] if j else None
        self.rate          = j["rate"] if j else None
        self.short_name    = j["cc"] if j else None
        self.exchange_date = j["exchangedate"] if j else None

    def __str__(self):
        return "%s (%s)  ₴ %f" % (self.short_name, self.full_name, self.rate)



class NbuData :
    def __init__(self):
        request = requests.get(url)
        response = request.json()
        self.rates = [NbuRate(j) for j in response]

    def size(self):
        return len(self.rates)
    
    def get_by_short_name(self, fragment:str) -> NbuRate | None:        
        return next(
            (rate for rate in self.rates if rate.short_name == fragment.upper()),
            None)
        
    def filter(self, fragment:str) :
        return (rate for rate in self.rates 
                if fragment.upper() in rate.short_name
                or fragment.upper() in rate.full_name.upper() )


def main() :
    nbu_data = NbuData()
    print("Loaded rates: ", nbu_data.size())
    fragment = input("Enter name to search: ")
    # r = nbu_data.get_by_short_name(fragment)
    # print( r if r else "Not found") 
    print(*nbu_data.filter(fragment), sep='\n')


if __name__ == '__main__' :
    main()


'''
Д.З. Модифікувати програму по роботі з курсами валют
забезпечити на початку програми введення користувачем
дати, на яку він хоче одержувати курси.
Документація по АРІ НБУ
https://bank.gov.ua/ua/open-data/api-dev
(розд. 1.3)

Одержати від користувача введену дату
> Введіть дату у форматі dd.mm.yy (Enter - поточна)

Перевірити її на валідність, а також на те, що вона з минулого
> Дата не розпізнана або майбутня
> Введіть дату у форматі dd.mm.yy (Enter - поточна)

Перетворити на формат для АРІ, виконати вибірку
Перейти до пошуку за фрагментом
'''