from django.urls import path

from . import views

app_name = 'popularity'

urlpatterns = [
    path('relationships', views.relations, name='all relationships'),
    path('graphdata', views.graphdata)
]