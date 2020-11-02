from django.db import models

# Create your models here.
class Bidang(models.Model):
    nama_bidang = models.CharField(max_length=120)
    kode_bidang = models.CharField(max_length=12)