from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .forms.demo_form import DemoForm

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


def forms(request) :
    template = loader.get_template('forms.html') 
    context = {
        'demo_form': DemoForm(request.POST) if request.method == 'POST' else DemoForm()
    }
    return HttpResponse(template.render(context, request))

'''
Д.З. Реалізувати стилізацію футера шаблону сторінок
- декоративна: додати тінь дзеркально-симетричну до заголовкової
- інформативна: футер повинен містити уставну інформацію
- навігаційна: необхідно забезпечити переходи на основні розділи сайту
'''