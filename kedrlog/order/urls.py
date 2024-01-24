from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('', views.index, name='index'),
    path('update-house/', views.update_total_section_house, name='update_total_section_house'),
    path('update-service/', views.update_total_section_service, name='update_total_section_service'),
    path('new/', views.new, name='new'),
    path('update/<int:deal_id>/', views.update, name='update'),
    path('delete/<int:deal_id>/', views.delete, name='delete'),
]
