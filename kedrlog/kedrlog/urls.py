from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from staticpages.views import page_gallery, page_text_content, page_price, page_spa

urlpatterns = [
    path('', include('mainpage.urls', namespace='mainpage')),
    path('personal/', include('personal.urls', namespace='personal')),
    path('accounts/', include('users.urls', namespace='accounts')),
    path('order/', include('order.urls', namespace='order')),
    path('houses/', page_gallery, name='houses'),
    path('territory/', page_gallery, name='territory'),
    path('food/', page_gallery, name='food'),
    path('rules/', page_text_content, name='rules'),
    path('fz152/', page_text_content, name='fz152'),
    path('accessories/', page_text_content, name='accessories'),
    path('price/', page_price, name='price'),
    path('spa/', page_spa, name='spa'),
    path('corporate/', page_text_content, name='corporate'),
    path('admin/', admin.site.urls),
]

if not settings.PRODUCTION:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
