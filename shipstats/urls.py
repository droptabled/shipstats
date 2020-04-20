from django.urls import include, path
from django.contrib import admin

from shipstats import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scraper/', include('scraper.urls')),
    path('popularity/', include('popularity.urls')),
    path('compare', views.compare),
    path('compare_ships', views.compare_ships)
]
