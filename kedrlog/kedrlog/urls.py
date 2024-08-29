from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from staticpages.views import (page_gallery, page_price, page_spa, page_gift_certificate, get_rate,
                               page_text_content, OrderGiftCertificateCreateView, OrderGiftCertificateDetailView)

urlpatterns = [
    path('', include('mainpage.urls', namespace='mainpage')),
    path('personal/', include('personal.urls', namespace='personal')),
    path('accounts/', include('users.urls', namespace='accounts')),
    path('order/', include('order.urls', namespace='order')),
    path('houses/', page_gallery, name='houses'),
    path('territory/', page_gallery, name='territory'),
    path('food/', page_gallery, name='food'),
    path('rules/', page_text_content, name='rules'),
    path('rules-gift-cert/', page_text_content, name='rules-gift-cert'),
    path('fz152/', page_text_content, name='fz152'),
    path('accessories/', page_text_content, name='accessories'),
    path('price/', page_price, name='price'),
    path('get-rate/', get_rate, name='get-rate'),
    path('spa/', page_spa, name='spa'),
    path('corporate/', page_text_content, name='corporate'),
    path('certificate/', page_gift_certificate, name='certificate'),
    path('create-cert/<int:gift_cert_id>/', OrderGiftCertificateCreateView.as_view(), name='create-cert'),
    path('ok-cert/<int:pk>/', OrderGiftCertificateDetailView.as_view(), name='ok-cert'),
    path('admin/', admin.site.urls),
]

if not settings.PRODUCTION:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
