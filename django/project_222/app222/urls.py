from django.urls import path
from . import views

urlpatterns = [
    path('',          views.home,     name='index'   ),
    path('forms/',    views.forms,    name='forms'   ),
    path('hello/',    views.hello,    name='hello'   ),
    path('home/',     views.home,     name='home'    ),
    path('models/',   views.models,   name='models'  ),
    path('transfer/', views.transfer, name='transfer'),
]
