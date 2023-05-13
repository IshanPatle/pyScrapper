from django.urls import path 
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from. import views

from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('faq/', views.faq, name='faq'),
    path('loader/', views.loader, name='loader'),
    path('login/', views.login, name='login'),
    path('search/', views.search_results, name='search_results'),
    path('save_to_excel/', views.save_to_excel, name='save_to_excel'),

    url(r'^download/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    ]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)