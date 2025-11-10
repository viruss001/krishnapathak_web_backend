from django.db import models

class Blog(models.Model):
    image = models.ImageField(upload_to='blogs/')
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
