from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),
    path('transfer/', views.transfer, name='transfer'),
]
