# Generated by Django 3.1.1 on 2020-10-07 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pegawai',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nik', models.CharField(max_length=12)),
                ('nik_sap', models.CharField(max_length=12)),
                ('nama', models.CharField(max_length=128)),
                ('p_grade', models.CharField(blank=True, max_length=4, null=True)),
                ('job_grade', models.CharField(blank=True, max_length=4, null=True)),
                ('grade_sap', models.CharField(blank=True, max_length=4, null=True)),
                ('nama_jabatan', models.CharField(blank=True, max_length=128, null=True)),
                ('jabatan', models.CharField(blank=True, max_length=5, null=True)),
                ('kode_unitkerja', models.CharField(blank=True, max_length=10, null=True)),
                ('kode_dir', models.CharField(blank=True, max_length=10, null=True)),
                ('kode_komp', models.CharField(blank=True, max_length=10, null=True)),
                ('kode_dept', models.CharField(blank=True, max_length=10, null=True)),
                ('kode_bagian', models.CharField(blank=True, max_length=10, null=True)),
                ('kode_seksi', models.CharField(blank=True, max_length=10, null=True)),
                ('direktorat', models.CharField(blank=True, max_length=128, null=True)),
                ('kompartemen', models.CharField(blank=True, max_length=128, null=True)),
                ('departemen', models.CharField(blank=True, max_length=128, null=True)),
                ('bagian', models.CharField(blank=True, max_length=128, null=True)),
                ('seksi', models.CharField(blank=True, max_length=128, null=True)),
                ('regu', models.CharField(blank=True, max_length=128, null=True)),
                ('poscode', models.CharField(blank=True, max_length=24, null=True)),
                ('postitle', models.CharField(blank=True, max_length=128, null=True)),
                ('alamat', models.CharField(blank=True, max_length=128, null=True)),
                ('kelurahan', models.CharField(blank=True, max_length=128, null=True)),
                ('kecamatan', models.CharField(blank=True, max_length=128, null=True)),
                ('kabupaten', models.CharField(blank=True, max_length=128, null=True)),
                ('provinsi', models.CharField(blank=True, max_length=64, null=True)),
                ('kode_pos', models.CharField(blank=True, max_length=8, null=True)),
                ('lp', models.CharField(blank=True, max_length=12, null=True)),
                ('nik_bp', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
    ]