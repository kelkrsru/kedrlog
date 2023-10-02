from django.urls import path

from . import views

app_name = 'personal'

urlpatterns = [
    path('', views.index, name='index'),
    path('reserve/', views.reserve, name='reserve'),
    path('bonus/', views.bonus, name='bonus'),
]
