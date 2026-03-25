from typing import Any
from django import forms

class DemoForm(forms.Form):        # форми задаються класами, 
    name = forms.CharField(        # спадкування від forms.Form
        label="Ім'я",              # надає ряд можливостей
        required=True,
        min_length=2,
        max_length=16,
        error_messages={
            'required': "Необхідно зазначити ваше ім'я",
            'min_length': "Введене ім'я закоротке: має бути принаймні 2 літери",
            'max_length': "Введене ім'я задовге: обмежтесь 16 літерами",
        })
    surname = forms.CharField(
        label="Прізвище",
        required=True,
        min_length=2,
        max_length=16,
        error_messages={
            'required': "Необхідно зазначити ваше прізвище",
            'min_length': "Введене прізвище закоротке: має бути принаймні 2 літери",
            'max_length': "Введене прізвище задовге: обмежтесь 16 літерами",
        })
    
    # Розширена (custom) валідація - переозначення методу clean
    def clean(self) -> dict[str, Any]:       # метод формує dict з іменами полів форми та 
        cleaned_values = super().clean()     # значеннями, що їм надаються (після дообробки)
        if 'name' in cleaned_values :        # Наявність поля у dict означає, що попередня перевірка пройдена
            # замість прямого посилання на self.name краще орієнтуватись на значення,
            # що поміщене до cleaned_values, оскільки воно може бути дооброблене
            name = cleaned_values['name']
            # Доповнимо перевіркою того, що перша літера імені має бути великою
            if not name[0].isupper():
                # додаємо помилку валідації з власним повідомленням
                self.add_error('name', forms.ValidationError("Ім'я має починатись з великої літери"))

        return cleaned_values
    
