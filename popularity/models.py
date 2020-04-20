from django.db import models
from scraper import models as sm
import datetime, decimal

class ShipRelation(models.Model):
    ship_primary = models.ForeignKey(sm.Ship, related_name='%(class)s_primary', on_delete=models.CASCADE)
    ship_secondary = models.ForeignKey(sm.Ship, related_name='%(class)s_secondary',on_delete=models.CASCADE)
    playercount = models.IntegerField()
    ship1median = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    ship2median = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    def update_edge(self):
        #temporary plot to use extract_stats
        plot = sm.Plot(ship_primary = self.ship_primary, ship_secondary = self.ship_secondary)
        stats = plot.extract_stats()
        self.playercount = len(stats)
        stats.sort(key=lambda x: x[1][0])
        self.ship1median = stats[round(self.playercount/2)][1][0]
        stats.sort(key=lambda x: x[1][1])
        self.ship2median = stats[round(self.playercount/2)][1][1]
        self.save()
        
    def get_edge(self):
        if datetime.datetime.now(datetime.timezone.utc) - self.updated_at > datetime.timedelta(days = 1):
            self.update_edge()
        #define this as the performance of players who have both ships vs
        #the performance of those who own either/or both ships, averaged between both nodes
        #must cast to decimal since ship1median is a float if generated, decimal if extracted from db
        perfratio = (decimal.Decimal(self.ship1median) / decimal.Decimal(self.ship_primary.median_wr) + decimal.Decimal(self.ship2median) / decimal.Decimal(self.ship_secondary.median_wr))/2
        return {
            'ship1median': self.ship1median,
            'ship2median': self.ship2median,
            'playercount': self.playercount,
            'source': self.ship_primary.pk,
            'target': self.ship_secondary.pk,
            'perfratio': perfratio
        }

