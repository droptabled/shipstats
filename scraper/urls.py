from django.urls import path

from . import views

app_name = 'scraper'

urlpatterns = [
    path('', views.index, name='index'),
    path('poll', views.index, name='index'),
    path('scrape', views.scrape, name='scrape'),
    path('scrapestart', views.scrapestart, name='scrapestart'),
    path('scrapeall', views.scrapeall, name='scrapeall'),
    path('maintenance', views.maintenance)
]