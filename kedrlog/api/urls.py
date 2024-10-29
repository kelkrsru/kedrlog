from django.urls import path, include
from rest_framework import routers

from api import views

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'rate', views.RateViewSet, basename='rate')
router.register(r'price', views.PriceViewSet, basename='price')

urlpatterns = [
    path('v1/', include(router.urls)),
]
