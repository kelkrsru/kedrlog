from api import views
from django.urls import include, path
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'rate', views.RateViewSet, basename='rate')
router.register(r'price', views.PriceViewSet, basename='price')

urlpatterns = [
    path('v1/', include(router.urls)),
]
