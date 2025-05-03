from django.urls import path
from diploma import views

urlpatterns = [
    path("", views.home, name="home"),
]