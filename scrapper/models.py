from django.db import models


# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return '{}'.format(self.name)

    def nose(self):
        return 1
