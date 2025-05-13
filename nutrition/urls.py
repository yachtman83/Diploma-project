from django.urls import path
from .views import input_view

urlpatterns = [
    path("calculator/", input_view, name="nutrition_calculator"),
]
