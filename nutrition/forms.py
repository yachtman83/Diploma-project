from django import forms

class PreferenceForm(forms.Form):

     HEALTH_CHOICES = [
        ('gastritis', 'Гастрит'),
        ('hypertension', 'Гипертония'),
        ('allergy', 'Аллергия'),
        ('healthy', 'Нет'),
    ]
     health_profile = forms.ChoiceField(choices=HEALTH_CHOICES, label='Особые указания')
     
     calorie_goal = forms.IntegerField(
        label="Целевая калорийность",
        min_value=100,  # можно поставить меньше или убрать
        max_value=5000,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'input--style-2 no-spinner',
            'placeholder': 'Например, 250',
            'style': 'width: 100%;'
    })
    )
     exclude_ingredients = forms.CharField(label="Исключить продукты (через запятую)", required=False)