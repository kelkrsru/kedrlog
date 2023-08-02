from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path('', include('main.urls', namespace='reports')),
    # path('install/', include('core.urls', namespace='core')),
    # path('quotecard/', include('quotecard.urls', namespace='quotecard')),
    # path('reports/', include('reports.urls', namespace='reports')),
    path('admin/', admin.site.urls),
]
