# Анонімні функції / функціональні вирази / Lambda
# Синтаксично коректний набір операторів та їх операндів
# Інструкції (statements) - що не має результату
# Вирази (expressions) - що має результат

from functools import reduce


lam1 = lambda : print("I am Lambda")
x = 10
lam2 = None
lam3 = None
lam4 = None

def make_lam2() -> None :
    global lam2
    lam2 = lambda : print("x =", x)


def make_lam3() -> None :
    global lam3
    x = 20
    lam3 = lambda : print("x =", x)


def make_lam4() -> None :               # Висновки: відбувається автоматичний захват (capture)
    global lam4                         # локальних областей на момент створення лямбди.
    x = 40                              # Але момент захвату - це момент руйнації локальної області
    lam4 = lambda : print("x =", x)     # а не момент самого оголошення
    lam4()                              #   40 - у момент запуску область існує, захвату немає
    x = 50                              # Тобто для lam4 захват буде після x = 50  


def apply(lam, data) :
    return lam(data)


def main() :
    lam1()
    # IIFE вирази миттєвого запуску - дозволяють створювати
    # "одноразові" дії без залишку у пам'яті. Наприклад, завантажувачі
    (lambda : print("I am IIFE"))()
    x = 30
    make_lam2()    # 10
    lam2()
    make_lam3()    # 20
    lam3()
    make_lam4()    # 50
    lam4()
    lam5 = lambda a, b: a + b   # параметри (за потреби) - до ":", return не пишеться
    print(lam5(1,2))
    data = (1,2,3,4,5)
    mean_a = lambda d : reduce(lambda acc, b : acc + b, d, 0) / len(d)
    mean_g = lambda d : reduce(lambda acc, b : acc * b, d, 1.0) ** (1.0 / len(d))
    mean_h = lambda d : len(d) / reduce(lambda acc, b : acc + 1/b, d, 0) 
    print( apply(mean_a, data) )
    print( apply(mean_g, data) )
    print( apply(mean_h, data) )
    strategies = {
        "arithmetic": mean_a,
        "geometric": mean_g,
    }


if __name__ == '__main__' :
    main()


'''
Д.З. За допомогою lambda реалізувати дію подібну патерну "Стратегія" -
вибір алгоритму, який призводить до найбільшого (чи найменшого) результату,
якщо його прикладати до одних і тих самих даних.
- поєднати алгоритми розрахунку середніх значень до єдиної структури strategies
- описати дві функції min_strategy(strategies, data) та max_strategy(strategies, data)
   які повертають назву стратегії, що дає відповідний результат, наприклад
   "arithmetic"
* додати до стратегій таку, що розраховує медіану та одержати результати
До звіту додати скріншоти роботи програми   
'''