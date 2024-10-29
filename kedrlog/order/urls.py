from django.urls import path

from order import views

app_name = 'order'

urlpatterns = [
    path('', views.index, name='index'),
    path('get-price/', views.get_price_for_date, name='get-price'),
    path('get-settings-interval/', views.get_settings_interval, name='get-settings-interval'),
    path('new/', views.new, name='new'),
    path('update/<int:deal_id>/', views.update, name='update'),
    path('delete/<int:deal_id>/', views.delete, name='delete'),
]
