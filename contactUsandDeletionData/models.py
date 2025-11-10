from django.db import models

# Create your models here.
class ContactUs(models.Model):
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    YourEmail= models.EmailField()
    PhoneNumber=models.CharField(max_length=12)
    Subject=models.CharField(max_length=100)
    message=models.TextField()


class Deletiondata(models.Model):
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    YourEmail= models.EmailField()
    PhoneNumber=models.CharField(max_length=12)
    message=models.TextField()