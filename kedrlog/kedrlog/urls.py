from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from staticpages.views import page_gallery, page_text_content

urlpatterns = [
    path('', include('mainpage.urls', namespace='mainpage')),
    path('personal/', include('personal.urls', namespace='personal')),
    path('accounts/', include('users.urls', namespace='accounts')),
    path('houses/', page_gallery, name='houses'),
    path('territory/', page_gallery, name='territory'),
    path('food/', page_gallery, name='food'),
    path('rules/', page_text_content, name='rules'),
    path('accessories/', page_text_content, name='accessories'),
    path('rent/', page_text_content, name='rent'),

    # path('accounts/', include('django.contrib.auth.urls')),
    # path('quotecard/', include('quotecard.urls', namespace='quotecard')),
    # path('reports/', include('reports.urls', namespace='reports')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)