from django.urls import path 
from django.contrib import admin
from django.conf import settings
from django.urls import re_path
from django.views.static import serve
from django.conf import settings
from . import views
from django.conf.urls.static import static
from .views import save_to_excel, search
from .views import search, save_to_excel



urlpatterns = [
    path('', views.index, name='index'),
    path('faq/', views.faq, name='faq'),
    path('search_faq/', views.search_faq, name='search_faq'),
    
    path('loader/', views.loader, name='loader'),
    path('login/', views.login, name='login'),
    path('search/', views.search, name='search'),
    path('save-to-excel/', views.save_to_excel, name='save-to-excel'),
    re_path(r'^download/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)