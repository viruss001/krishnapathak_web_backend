from django.db import models

# Create your models here.
class PriceSection(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    validity = models.CharField(max_length=50)
    offer = models.CharField(max_length=50)

class BulletPoints(models.Model):
    title = models.ForeignKey(PriceSection,on_delete=models.CASCADE,related_name="bullet")
    points = models.CharField(max_length=500)
    