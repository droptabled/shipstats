from django.urls import path

from . import views

app_name = 'scraper'

urlpatterns = [
    path('poll', views.index, name='index'),
    path('scrape', views.scrape, name='scrape')
]