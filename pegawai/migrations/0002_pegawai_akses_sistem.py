# Generated by Django 3.1.1 on 2020-10-07 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pegawai', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pegawai',
            name='akses_sistem',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]
