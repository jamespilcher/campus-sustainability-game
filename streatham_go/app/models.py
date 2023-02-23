from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=50)
    distance = models.IntegerField()
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)

    def __str__(self):
        return self.location
