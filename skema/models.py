from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Skema(models.Model):
    nama_skema = models.CharField(max_length=120)
    kode_skema = models.CharField(max_length=12)