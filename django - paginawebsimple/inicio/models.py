from django.db import models

# Create your models here.

class Perfiles(models.Model):
    mote = models.CharField(max_length=20)
    desc = models.CharField(max_length=250)
    mayorDeEdad = models.BooleanField()

    def __str__(self):
        return self.mote