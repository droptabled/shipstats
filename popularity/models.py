from django.db import models
from scraper import models as sm

class ShipRelation(models.Model):
    ship_primary = models.ForeignKey(sm.Ship, related_name='%(class)s_primary', on_delete=models.CASCADE)
    ship_secondary = models.ForeignKey(sm.Ship, related_name='%(class)s_secondary',on_delete=models.CASCADE)
    count = models.IntegerField()
    ship1median = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    ship2median = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    def update_edge(self):
        plot = sm.Plot(ship_primary = self.ship_primary, ship_secondary = self.ship_secondary)
        stats = plot.extract_stats()
        self.count = len(stats)
        stats.sort(key=lambda x: x[1][0])
        self.ship1median = stats[round(self.count/2)][0]
        stats.sort(key=lambda x: x[1][1])
        self.ship2median = stats[round(self.count/2)][1]
        self.save()
        
    def get_edge(self):
        if datetime.datetime.now(datetime.timezone.utc) - self.updated_at > datetime.timedelta(days = 1):
            self.update_edge()
        return {
            "ship1median": self.ship1median,
            "ship2median": self.ship2median,
            "count": self.count,
            "nation": self.nation,
            "source": self.ship_primary.pk,
            "target": self.ship_secondary.pk
        }

