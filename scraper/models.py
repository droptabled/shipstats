# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from collections import defaultdict
import math, json

class User(models.Model):
    wg_user = models.IntegerField(default=0, unique=True)
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

class Ship(models.Model):
    ship_id = models.BigIntegerField(default=0, db_index=True)
    name = models.CharField(max_length=200)

class UserStat(models.Model):
    wg_user = models.ForeignKey(User, to_field='wg_user', on_delete=models.CASCADE)
    ship_id = models.ForeignKey(Ship, on_delete=models.CASCADE)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

class Plot(models.Model):
    ship_primary = models.ForeignKey(Ship, related_name='%(class)s_primary', on_delete=models.CASCADE)
    ship_secondary = models.ForeignKey(Ship, related_name='%(class)s_secondary', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    
    class PlotType(models.IntegerChoices):
        NONE = 0
        BOX = 1
        SCATTER = 2

    plot_type = models.IntegerField(choices=PlotType.choices)
    
    def extract_stats(self):
        ship_primary_stats = UserStat.objects.filter(ship_id__exact = self.ship_primary)
        ship_secondary_stats = UserStat.objects.filter(ship_id__exact = self.ship_secondary)
        primary_ids = set(ship_primary_stats.values_list('wg_user', flat=True))
        secondary_ids = set(ship_secondary_stats.values_list('wg_user', flat=True))
        
        update_list = list(primary_ids.intersection(secondary_ids))
        
        filtered_primary_stats = ship_primary_stats.filter(wg_user__in=update_list)
        filtered_secondary_stats = ship_secondary_stats.filter(wg_user__in=update_list)
        
        primary_wrs = dict(map(lambda x: (x.wg_user_id, (x.wins/(x.losses+x.wins))), filtered_primary_stats))
        secondary_wrs = dict(map(lambda x: (x.wg_user_id, (x.wins/(x.losses+x.wins))), filtered_secondary_stats))
        
        dd = defaultdict(list)
        for value in primary_wrs.items():
            dd[value[0]].append(value[1])
        for value in secondary_wrs.items():
            dd[value[0]].append(value[1])
        
        #kick out any items that don't have a matching pair somehow
        final_list = list(dd.items())
        for idx, val in enumerate(final_list):
            if len(val[1]) != 2:
                final_list.pop(idx) 
        return final_list
        
    def update_plot(self):
        stats = self.extract_stats()
        if self.plot_type == Plot.PlotType.BOX:
            stats.sort(key=lambda x: x[1][0])
            count = len(stats)
            segments = min(math.floor(count/50), 40)
            increment = math.floor(count/segments)

            for percentile in range(segments):
                percentile_stat = BoxPlotStat.objects.get_or_create(
                    plot = self,
                    ship_top_range = (percentile + 1) * (1 / segments)
                )[0]

                subset_stats = stats[percentile * increment : (percentile + 1) * increment]
                
                percentile_stat.ship_primary_5th = subset_stats[round(increment*0.05)][1][0]
                percentile_stat.ship_primary_95th = subset_stats[round(increment*0.95)][1][0]
                percentile_stat.ship_primary_q1 = subset_stats[round(increment*0.25)][1][0]
                percentile_stat.ship_primary_q3 = subset_stats[round(increment*0.75)][1][0]
                percentile_stat.ship_primary_median = subset_stats[round(increment*0.5)][1][0]
                
                
                # resort based on second ship wr to determine its boxplot
                subset_stats.sort(key=lambda x: x[1][1])
                percentile_stat.ship_secondary_5th = subset_stats[round(increment*0.05)][1][1]
                percentile_stat.ship_secondary_95th = subset_stats[round(increment*0.95)][1][1]
                percentile_stat.ship_secondary_q1 = subset_stats[round(increment*0.25)][1][1]
                percentile_stat.ship_secondary_q3 = subset_stats[round(increment*0.75)][1][1]
                percentile_stat.ship_secondary_median = subset_stats[round(increment*0.5)][1][1]
                percentile_stat.save()
        
        if self.plot_type == Plot.PlotType.SCATTER:
            percentile_stat = RawPlotStat.objects.get_or_create(plot = self)[0]
            percentile_stat.ship_json = json.dumps(list(map(lambda x: [round(x[1][0], 5), round(x[1][1], 5)], stats)))
            percentile_stat.save()

class CommonPlotStat(models.Model):
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    class Meta:
        abstract = True

class BoxPlotStat(CommonPlotStat):
    ship_top_range = models.DecimalField(max_digits=6, decimal_places=5, default=0)

    ship_primary_5th = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    ship_primary_95th = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    ship_primary_q1 = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    ship_primary_q3 = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    ship_primary_median = models.DecimalField(max_digits=6, decimal_places=5, default=0)

    ship_secondary_5th = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    ship_secondary_95th = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    ship_secondary_q1 = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    ship_secondary_q3 = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    ship_secondary_median = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    
class RawPlotStat(CommonPlotStat):
    ship_json = models.TextField()