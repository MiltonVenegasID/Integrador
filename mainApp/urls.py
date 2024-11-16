from django.urls import path, include
from mainApp.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls.static import static
from pwa import views as pwa_views

urlpatterns = [
    path('offline/', cache_page(settings.PWA_APP_NAME)(pwa_views.OfflineView.as_view())),
    path('Inicio', Inicio.as_view(), name = 'Inicio'),
    path('Chat', get_bot_response, name='Comm')
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
