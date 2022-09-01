from django.db import models


class Forecast(models.Model):
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    title = models.CharField(max_length=50, default="no title")
    mean = models.DecimalField(decimal_places=1, max_digits=3)
    variance = models.DecimalField(decimal_places=1, max_digits=3)
