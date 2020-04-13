# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse, JsonResponse
from django.template import loader
from scraper import models
import datetime

def compare(request):
    ships = models.Ship.objects.all().order_by("name")
    return render(request, 'shipstats/compare.html', {'ships': ships})

def compare_ships(request):
    try:
        ship_1 = models.Ship.objects.get(pk = request.GET['ship1'])
        ship_2 = models.Ship.objects.get(pk = request.GET['ship2'])
    # if the object doesn't exist return empty json string
    except ObjectDoesNotExist:
        return serializers.serialize("json", {})
    
    plot, created = models.Plot.objects.get_or_create(ship_primary = ship_1, ship_secondary = ship_2, plot_type = int(request.GET['type']))
 
    if created or (datetime.datetime.now(datetime.timezone.utc) - plot.updated_at > datetime.timedelta(days = 1)):
        plot.update_plot()
        plot.save()
    
    if int(request.GET['type']) == models.Plot.PlotType.BOX:
        plot_data = models.BoxPlotStat.objects.filter(plot = plot).values()
        return JsonResponse(list(plot_data), safe = False)
    elif int(request.GET['type']) == models.Plot.PlotType.SCATTER:
        plot_data = models.RawPlotStat.objects.get(plot = plot)
        return JsonResponse(plot_data.ship_json, safe = False)
    
