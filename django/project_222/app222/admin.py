from django.contrib import admin
from .models import *

# Register your models here.
# Оголошення моделей у models.py переносить їх до БД (міграціями)
# проте, для роботи з адміністративною панеллю їх також треба
# реєструвати у даному файлі

# admin.site.register(User)  # така реєстрація додає модель, але вона
# відображається без деталей ( User object (1) )

class UserAdminView(admin.ModelAdmin) :   # клас, що деталізує роботу з моделлю
    list_display = ('id', 'name', 'surname')

admin.site.register(User, UserAdminView)    