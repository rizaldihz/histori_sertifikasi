from django.db import models
from pegawai.models import Pegawai
from bidang.models import Bidang
from penyelenggara.models import Penyelenggara
from skema.models import Skema

class Sertifikasi(models.Model):
    pegawai = models.ForeignKey(Pegawai, on_delete=models.CASCADE, default=None)
    topik_sertifikasi = models.CharField(max_length=128, blank=True, null=True)
    bidang = models.ForeignKey(Bidang, on_delete=models.SET_NULL, blank=True, null=True)
    skema = models.ForeignKey(Skema, on_delete=models.SET_NULL, blank=True, null=True)
    penyelenggara = models.ForeignKey(Penyelenggara, on_delete=models.SET_NULL, blank=True, null=True)
    mulai_pelaksanaan = models.DateField(blank=True, null=True)
    akhir_pelaksanaan = models.DateField(blank=True, null=True)
    mulai_berlaku = models.DateField(blank=True, null=True)
    akhir_berlaku = models.DateField(blank=True, null=True)
    tipe = models.CharField(max_length=9,default=None)


    