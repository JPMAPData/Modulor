from django.db import models

# Create your models here.

class Bim(models.Model):
    acc_id = models.CharField(max_length=50)
    acc_secret = models.CharField(max_length=50)
    file = models.FileField()

