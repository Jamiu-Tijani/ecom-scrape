from django.db import models

# Create your models here.


class Products(models.Model):
    title = models.CharField(max_length=5000)
    price = models.CharField(max_length=5000)
    url = models.CharField(max_length=5000)
    source = models.CharField(max_length=5000, default="ebay")
