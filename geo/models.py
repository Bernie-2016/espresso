from django.contrib.gis.db import models


class CongressionalDistricts(models.Model):
    gid = models.AutoField(primary_key=True)
    district = models.CharField(max_length=2, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    party = models.CharField(max_length=19, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    stfips = models.CharField(max_length=2, blank=True, null=True)
    statedist = models.CharField(max_length=4, blank=True, null=True)
    geom = models.MultiPolygonField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'congressional_districts'

    def __unicode__(self):
        return ' '.join([self.state, self.district])