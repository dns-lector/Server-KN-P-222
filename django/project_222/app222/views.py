from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# Create your views here.                   # Представлення - це функції, які готують дані для шаблонів
def hello(request) :                        # або без шаблонів формують відповідь (у ASP їх аналог - контролер/action)
    return HttpResponse("Hello, World!")    # 

def home(request) :
    template = loader.get_template('home.html')  # директорія templates визначається автоматично
    return HttpResponse(template.render())

def transfer(request) :
    template = loader.get_template('transfer.html')
    context = {                                         # Контекст (у даному сенсі) - набір даних для 
        'x': 10,                                        # шаблона представлення (в ASP таке називають ViewModel)
        'str': 'The string'                             # 
    }
    context['all'] = context
    return HttpResponse(template.render(context, request))

'''
Д.З. Створити сторінку з інструкцією встановлення і налаштування Django,
у контексті передати дані про поточні дату-час,
вивести на сторінці повідомлення: "матеріали відображені 11.03.2026 о 10:05"
'''