class Point :                     # На відміну від більшості ООП-мов, у яких this - неявний 
    def __init__(self,            # параметр методів, у Python він передається явно і традиційно      
            x:float=0.0,          # називається self. Через нього можна створювати саме об'єктні
            y:float=0.0):         # поля. Конструктор класу носить спец.назву __init__
        self.x = x                # Методи класів (як і функції) не перевантажуються, за потреби
        self.y = y                # поліморфізму вживаються параметри за замовчанням
                                  # 
    def __str__(self):            # Спец.методи класу задають його поведінку, зокрема, рядкове представлення
        return "(%.2f,%.2f)" % (  # __str__ - аналог .toString()
            self.x, self.y)
    
    def __repr__(self):
        return "(%f,%f)" % (      # representer - для виведення у складі інших об'єктів
            self.x, self.y)
    
    def magnitude(self) :         # в оголошенні наших методів self необхідний, 
        return (self.x ** 2 +     # він завжди є першим параметром, проте, при
            self.y ** 2) ** 0.5   # виклику цей параметр не зазначається
    
    def distance_to(self, other) :
        'Обчислення відстані між точками'  # документучий коментар - як і в функціях - перший рядок
        return ((self.x - other.x) ** 2    # після оголошення функції
              + (self.y - other.y) ** 2 ) ** 0.5
                                      # ряд спецметодів відповідає за операції з даними об'єктами
    def __add__(self, other) :        # зокрема, __add__ - для оператора "+" 
        if isinstance(other, Point):  # Відсутність вбудованої типізації вимагає забезпечення її
            return Point(             # у методах
                self.x + other.x,
                self.y + other.y
            )
        else :
            raise TypeError("Unsupported '+' operands type: Point and " + str(type(other)))

    def __sub__(self, other) : 
        return Point(             # __sub__ - для оператора "-" 
            self.x - other.x,
            self.y - other.y
        )
    
    def __mul__(self, other):
        '''Множення: множення на число повертає нову точку, у 
        якій кожна координата збільшена у відповідне число;
        множення на іншу точку відповідає скалярному добутку
        і повертає числовий результат'''
        if isinstance(other, Point) :
            return self.x * other.x + self.y * other.y
        elif isinstance(other, (int, float)):
            return Point(self.x * other, self.y * other)
        else :
            raise TypeError("Unsupported '*' operands type: Point and " + str(type(other)))
        
    def __truediv__(self, other):            # operator "/"
        if isinstance(other, (int,float)) :
            if other == 0 :
                raise ZeroDivisionError("Cannot divide by zero")
            return Point(self.x / other, self.y / other)
        else :
            raise TypeError("Unsupported '/' operands type: Point and " + str(type(other)))



def main():
    p1 = Point()    
    print(p1)                    # (0.00,0.00) -- дія методу __str__
    d = {'p2': Point()}          # на внутрішнє представлення діє не __str__ а __repr__
    print(d)                     # без __repr__ -- {'p2': <__main__.Point object at 0x000001D88C828A50>}
    p1.x = 3
    p1.y = 4                     # хоча методи оголошуються з (self), їх виклик
    print(p1.magnitude())        # здійснюється без цього параметра
    d['p2'].x = 1                # Коли метод оголошений з двома параметрами,           
    d['p2'].y = 1                # перший - self, а при виклику зазначається тільки
    print(p1.distance_to(d['p2']))  # один, який зв'язується з другим  
    p2 = Point(2,4)                 # Позиційне зв'язування - за порядком оголошення
    print(p1.distance_to(p2))
    p3 = Point(y=2)                 # Іменоване зв'язування - за іменем параметра
    print("p3 =", p3)               # p3 = (0.00,2.00) -- x - за замовчанням, у - за значенням
    print("p1 = %s, p2 = %s, p1+p2 = %s" % (p1, p2, p1 + p2))
    print("p1 = %s, p2 = %s, p1-p2 = %s" % (p1, p2, p1 - p2))
    print("p1 = %s, p2 = %s, p1*p2 = %s" % (p1, p2, p1 * p2))
    print("p1 = %s, p2 = %s, p1*2 = %s" % (p1, p2, p1 * 2))
    print("p1 = %s, p2 = %s, p1/2 = %s" % (p1, p2, p1 / 2))



if __name__ == '__main__':
    main()
