from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from sertifikasi.models import Sertifikasi
from django.db.models import Q
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from bidang.models import Bidang
from penyelenggara.models import Penyelenggara
from pegawai.models import Pegawai
from skema.models import Skema

from django.db.models import Q, Count

from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
import locale
from django.db.models.functions import Trunc

import re
import datetime
import random
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from math import ceil

# Create your views here.
def grafik_view(request, *args, **kwargs):
    return render(request, 'laporan/grafik.html', {})

def pivot_view(request, *args, **kwargs):
    return render(request, 'laporan/pivot.html', {})

class QueryJSON(BaseDatatableView):
    order_columns = ['nomor','pegawai__nik','pegawai__nama','jumlah']
    max_display_length = 200
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

    def get_initial_queryset(self):
        if 'mulai' in self.request.GET and 'hingga' in self.request.GET:
            tgl_akhir_str = self.request.GET.get('hingga', None)
            tgl_mulai_str = self.request.GET.get('mulai', None)
            tgl_akhir = datetime.datetime.strptime(tgl_akhir_str,"%d-%m-%Y")
            tgl_mulai = datetime.datetime.strptime(tgl_mulai_str,"%d-%m-%Y")
        else:
            tgl_akhir = datetime.datetime.strptime('01-01-0001',"%d-%m-%Y")
            tgl_mulai = datetime.datetime.today()
        q_obj = Sertifikasi.objects.filter(akhir_berlaku__gte=tgl_akhir.date(),mulai_berlaku__lte=tgl_mulai.date()).prefetch_related('pegawai')
        return q_obj.values('pegawai__nama','pegawai__nik').annotate(jumlah = Count('pegawai__nama'))

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(pegawai__nama__icontains=search)
        return qs
    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                None,  # escape HTML for security reasons
                item['pegawai__nik'],
                item['pegawai__nama'],
                item['jumlah'],
            ])
        return json_data

def colorGen(number):
    number = hash(str(number))
    r = ((number & 0x00FFFFFF) >> 16) % 256
    g = ((number & 0x00FFFFFF) >> 8) % 256
    b = ((number & 0x00FFFFFF)) % 256
    return r,g,b

def chartQuery(request, *args, **kwargs):
    if request.method == 'GET':
        tipe_chart = request.GET.get('chart', None)
        
        saat_ini = datetime.datetime.today()
        tahun_ini = saat_ini.strftime("%Y")

        direktorat_q = Pegawai.objects.values('direktorat').distinct()
        if tipe_chart == 'line-1':
            hasil = {}
            count = 0
            for k in direktorat_q:
                count+=1
                r,g,b = colorGen(count)
                hasil[k['direktorat']] = {}
                hasil[k['direktorat']]['label'] = k['direktorat']
                hasil[k['direktorat']]['data'] = []
                hasil[k['direktorat']]['borderColor'] = f'rgba({r},{g},{b}, 0.7)'
                hasil[k['direktorat']]['backgroundColor'] = hasil[k['direktorat']]['borderColor']
                hasil[k['direktorat']]['fill'] = False
            
            locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
            labels = []
            for i in range(5):
                waktu_s = saat_ini + datetime.timedelta(days=(((i-2)*30)+1))
                waktu_s = waktu_s.replace(day=1)
                labels.append(waktu_s.strftime("%B %Y"))

                q_obj = Sertifikasi.objects.filter(akhir_berlaku__gte=waktu_s.date(),mulai_berlaku__lte=waktu_s.date()).prefetch_related('pegawai')
                count_q = q_obj.values('pegawai__direktorat').annotate(jumlah = Count('pegawai__direktorat'))
                for divisi in direktorat_q:
                    jumlah_q = count_q.filter(pegawai__direktorat=divisi['direktorat'])
                    jumlah = 0
                    if not jumlah_q.exists() : 
                        jumlah = 0
                    else : 
                        jumlah = jumlah_q[0]['jumlah']
                    hasil[divisi['direktorat']]['data'].append(jumlah)
            
            datasets = []
            for key in hasil:
                datasets.append(hasil[key])
            
            return JsonResponse(data={
                'labels': labels,
                'datasets': datasets,
            })

        if tipe_chart == 'line-2':
            hasil = {}
            count = 0
            kelompok = ['Aktif', 'Tidak Aktif', 'Total']
            for k in kelompok:
                count+=1
                r,g,b = colorGen(count)
                hasil[k] = {}
                hasil[k]['label'] = k
                hasil[k]['data'] = []
                hasil[k]['borderColor'] = f'rgba({r},{g},{b}, 0.7)'
                hasil[k]['backgroundColor'] = hasil[k]['borderColor']
                hasil[k]['fill'] = False
            
            locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
            labels = []
            for i in range(5):
                waktu_s = saat_ini + datetime.timedelta(days=(((i-2)*30)+1))
                waktu_s = waktu_s.replace(day=1)
                labels.append(waktu_s.strftime("%B %Y"))

                #aktif
                q_aktif = Sertifikasi.objects.filter(akhir_berlaku__gte=waktu_s.date(),mulai_berlaku__lte=waktu_s.date())
                count_aktif = q_aktif.count()
                hasil['Aktif']['data'].append(count_aktif)

                #tidak
                q_n_aktif = Sertifikasi.objects.filter(akhir_berlaku__lt=waktu_s.date(), mulai_berlaku__lt=waktu_s.date())
                count_n_aktif = q_n_aktif.count()
                hasil['Tidak Aktif']['data'].append(count_n_aktif)

                #total
                q_tot = Sertifikasi.objects.filter(mulai_berlaku__lte=waktu_s.date())
                count_tot = q_tot.count()
                hasil['Total']['data'].append(count_tot)

            datasets = []
            for key in hasil:
                datasets.append(hasil[key])
            
            return JsonResponse(data={
                'labels': labels,
                'datasets': datasets,
            })
        
        if tipe_chart == 'pie':
            labels = []
            data = []
            color = []
            waktu_s = saat_ini
            waktu_s = waktu_s.replace(day=1)
            q_obj = Sertifikasi.objects.filter(akhir_berlaku__gte=waktu_s.date(),mulai_berlaku__lte=waktu_s.date()).prefetch_related('pegawai')
            count_q = q_obj.values('pegawai__direktorat').annotate(jumlah = Count('pegawai__direktorat'))
            count = 0
            for divisi in direktorat_q:
                labels.append(divisi['direktorat'])
                jumlah_q = count_q.filter(pegawai__direktorat=divisi['direktorat'])
                jumlah = 0
                if not jumlah_q.exists() : 
                    jumlah = 0
                else : 
                    jumlah = jumlah_q[0]['jumlah']
                data.append(jumlah)
                count+=1
                r,g,b = colorGen(count)
                color.append(f'rgba({r},{g},{b},1)')
            
            return JsonResponse(data={
                'labels': labels,
                'data': data,
                'color' : color
            })
    
    if request.method == 'POST' and request.is_ajax:
        tgl_mulai_str = request.POST.get('mulai', None)
        tgl_akhir_str = request.POST.get('hingga', None)
        tgl_mulai = datetime.datetime.strptime(tgl_mulai_str,"%d-%m-%Y")
        tgl_akhir = datetime.datetime.strptime(tgl_akhir_str,"%d-%m-%Y")

        durasi = tgl_akhir - tgl_mulai
        n_bulan = int(durasi.days/30)

        #line1
        direktorat_q = Pegawai.objects.values('direktorat').distinct()
        hasil = {}
        count = 0
        for k in direktorat_q:
            count+=1
            r,g,b = colorGen(count)
            hasil[k['direktorat']] = {}
            hasil[k['direktorat']]['label'] = k['direktorat']
            hasil[k['direktorat']]['data'] = []
            hasil[k['direktorat']]['borderColor'] = f'rgba({r},{g},{b}, 0.7)'
            hasil[k['direktorat']]['backgroundColor'] = hasil[k['direktorat']]['borderColor']
            hasil[k['direktorat']]['fill'] = False
        locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
        labels = []
        for i in range(n_bulan):
            waktu_s = tgl_mulai + datetime.timedelta(days=(((i)*30)+1))
            waktu_s = waktu_s.replace(day=1)
            labels.append(waktu_s.strftime("%B %Y"))

            q_obj = Sertifikasi.objects.filter(akhir_berlaku__gte=waktu_s.date(), mulai_berlaku__lte=waktu_s.date()).prefetch_related('pegawai')
            count_q = q_obj.values('pegawai__direktorat').annotate(jumlah = Count('pegawai__direktorat'))
            for divisi in direktorat_q:
                jumlah_q = count_q.filter(pegawai__direktorat=divisi['direktorat'])
                jumlah = 0
                if not jumlah_q.exists() : 
                    jumlah = 0
                else : 
                    jumlah = jumlah_q[0]['jumlah']
                hasil[divisi['direktorat']]['data'].append(jumlah)
            
        datasets = []
        for key in hasil:
            datasets.append(hasil[key])

        #line-2
        hasil2 = {}
        count2 = 0
        kelompok2 = ['Aktif', 'Tidak Aktif', 'Total']
        for k in kelompok2:
            count2+=1
            r2,g2,b2 = colorGen(count)
            hasil2[k] = {}
            hasil2[k]['label'] = k
            hasil2[k]['data'] = []
            hasil2[k]['borderColor'] = f'rgba({r2},{g2},{b2}, 0.7)'
            hasil2[k]['backgroundColor'] = hasil2[k]['borderColor']
            hasil2[k]['fill'] = False
        
        locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
        labels2 = []
        for i in range(n_bulan):
            waktu_s = tgl_mulai + datetime.timedelta(days=(((i)*30)+1))
            waktu_s = waktu_s.replace(day=1)
            labels2.append(waktu_s.strftime("%B %Y"))

            #aktif
            q_aktif = Sertifikasi.objects.filter(akhir_berlaku__gte=waktu_s.date(),mulai_berlaku__lte=waktu_s.date())
            count_aktif = q_aktif.count()
            hasil2['Aktif']['data'].append(count_aktif)

            #tidak
            q_n_aktif = Sertifikasi.objects.filter(akhir_berlaku__lt=waktu_s.date(), mulai_berlaku__lt=waktu_s.date())
            count_n_aktif = q_n_aktif.count()
            hasil2['Tidak Aktif']['data'].append(count_n_aktif)

            #total
            q_tot = Sertifikasi.objects.filter(mulai_berlaku__lte=waktu_s.date())
            count_tot = q_tot.count()
            hasil2['Total']['data'].append(count_tot)

        datasets2 = []
        for key in hasil2:
            datasets2.append(hasil2[key])
        
        return JsonResponse(data=[{
            'labels': labels,
            'datasets': datasets,
        },{
            'labels': labels2,
            'datasets': datasets2,
        }], safe=False)