from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Penyelenggara(models.Model):
    nama_penyelenggara = models.CharField(max_length=120)
    kode_penyelenggara = models.CharField(max_length=12)