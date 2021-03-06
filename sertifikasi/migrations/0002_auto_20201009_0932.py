# Generated by Django 3.1.1 on 2020-10-09 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bidang', '0001_initial'),
        ('penyelenggara', '0001_initial'),
        ('skema', '0002_auto_20201007_1040'),
        ('pegawai', '0002_pegawai_akses_sistem'),
        ('sertifikasi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sertifikasi',
            name='nik',
        ),
        migrations.AddField(
            model_name='sertifikasi',
            name='akhir_berlaku',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sertifikasi',
            name='akhir_pelaksanaan',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sertifikasi',
            name='bidang',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bidang.bidang'),
        ),
        migrations.AddField(
            model_name='sertifikasi',
            name='mulai_berlaku',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sertifikasi',
            name='mulai_pelaksanaan',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sertifikasi',
            name='pegawai',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pegawai.pegawai'),
        ),
        migrations.AddField(
            model_name='sertifikasi',
            name='penyelenggara',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='penyelenggara.penyelenggara'),
        ),
        migrations.AddField(
            model_name='sertifikasi',
            name='skema',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='skema.skema'),
        ),
        migrations.AddField(
            model_name='sertifikasi',
            name='tipe',
            field=models.CharField(default=None, max_length=9),
        ),
        migrations.AddField(
            model_name='sertifikasi',
            name='topik_sertifikasi',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
