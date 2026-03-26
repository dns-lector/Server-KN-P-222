from django.db import models

# Create your models here.
# Моделі - це класи, призначені для відображення на БД
# а сам файл models можна порівняти з контекстом даних EF/ASP

class User(models.Model) :
    name = models.CharField(max_length=64)      # Зауважимо, що поле ID
    surname = models.CharField(max_length=64)   # ми не описуємо, проте
    birthdate = models.DateField(null=True)     # воно буде створено міграцією