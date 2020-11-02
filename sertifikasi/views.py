from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Sertifikasi
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

# Create your views here.
def beranda_view(request, *args, **kwargs):
    return render(request, 'beranda/beranda.html', {})

def daftar_sertifikasi_view(request, *args, **kwargs):
    return render(request, 'sertifikasi/daftar-sertifikasi.html', {})

def tambah_sertifikasi(request, *args, **kwargs):
    if request.method == "GET":
        return render(request, 'sertifikasi/tambah-sertifikasi.html', {})
    if request.method == "POST":
        if len(request.FILES) != 0:
            excel_file = request.FILES["excel_file"]
            if (str(excel_file)).split('.')[-1] == "xls" :
                data = xls_get(excel_file)
            elif (str(excel_file)).split('.')[-1] == "xlsx" :
                data = xlsx_get(excel_file)
            else:
                return redirect('daftar-sertifikasi')
            sertifikasi_s = data['Sheet1']
            # pegawai_non = []
            if len(sertifikasi_s) > 1: 
                iter = 1
                for sertifikasi in sertifikasi_s:
                    if len(sertifikasi) > 0:
                        if(sertifikasi[0]!='No.'):
                            try:
                                nik_str = re.sub('[\W_]+', '', str(sertifikasi[2]))
                                pegawai_obj = Pegawai.objects.filter(Q(nik=nik_str) | Q(nik_sap=nik_str)).first() if nik_str is not None else None
                                bidang_obj = Bidang.objects.filter(nama_bidang=sertifikasi[5]).first() if sertifikasi[5] is not None else None
                                skema_obj = Skema.objects.filter(nama_skema=sertifikasi[6]).first() if sertifikasi[6] is not None else None
                                penyelenggara_obj = Penyelenggara.objects.filter(nama_penyelenggara=sertifikasi[7]).first() if sertifikasi[7] is not None else None
                                if pegawai_obj is not None:
                                    Sertifikasi.objects.create(
                                        pegawai = pegawai_obj,
                                        bidang = bidang_obj if bidang_obj is not None else None,
                                        penyelenggara = penyelenggara_obj if penyelenggara_obj is not None else None,
                                        skema = skema_obj if skema_obj is not None else None,
                                        topik_sertifikasi = sertifikasi[4] if sertifikasi[4] is not None else None,
                                        mulai_pelaksanaan = assert_date(sertifikasi[8]),
                                        akhir_pelaksanaan = assert_date(sertifikasi[9]),
                                        mulai_berlaku = assert_date(sertifikasi[10]),
                                        akhir_berlaku = assert_date(sertifikasi[11]),
                                        tipe = sertifikasi[12]
                                    )
                                else:
                                    print(f'pegawai not found {nik_str}')
                                    # if sertifikasi[2] not in pegawai_non: pegawai_non.append(sertifikasi[2])
                                
                            except Exception as e:
                                print(f"{iter} {e} {nik_str}")
                    iter+=1
                # for z in pegawai_non:
                #     print(z)
                return redirect('sertifikasi:tambah-sertifikasi')


def assert_date(params):
    res = None
    try:
        res = params.date()
    except Exception as e:
        res = None
    return res

class QueryJSON(BaseDatatableView):
    model = Sertifikasi
    columns = ['nomor','pegawai.nama','pegawai.nik','pegawai.departemen','topik_sertifikasi','tipe','penyelenggara.nama_penyelenggara','bidang.nama_bidang','skema.nama_skema','mulai_pelaksanaan','akhir_pelaksanaan','mulai_berlaku','akhir_berlaku']
    order_columns = ['nomor','pegawai.nama','pegawai.nik','pegawai.departemen','topik_sertifikasi','tipe','penyelenggara.nama_penyelenggara','bidang.nama_bidang','skema.nama_skema','mulai_pelaksanaan','akhir_pelaksanaan','mulai_berlaku','akhir_berlaku']
    max_display_length = 200
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

    def render_column(self, row, column):
        if column == 'tipe' :
            if row.tipe == 'BNSP':
                return '<span class="badge badge-warning">{0}</span>'.format(row.tipe)
            return '<span class="badge badge-primary">{0}</span>'.format(row.tipe)
        if column == 'mulai_pelaksanaan' : return "" if row.mulai_pelaksanaan is None else row.mulai_pelaksanaan.strftime("%d %B %Y")
        if column == 'akhir_pelaksanaan' : return "" if row.akhir_pelaksanaan is None else row.akhir_pelaksanaan.strftime("%d %B %Y")
        if column == 'mulai_berlaku' : return "" if row.mulai_berlaku is None else row.mulai_berlaku.strftime("%d %B %Y")
        if column == 'akhir_berlaku' : return "" if row.akhir_berlaku is None else row.akhir_berlaku.strftime("%d %B %Y")
        return super(QueryJSON, self).render_column(row, column)

def colorGen(string):
    number = (hash(string))
    r = ((number & 0x00FFFFFF) >> 16) % 256
    g = ((number & 0x00FFFFFF) >> 8) % 256
    b = ((number & 0x00FFFFFF)) % 256
    return r,g,b

def chartQuery(request, *args, **kwargs):
    tipe_chart = request.GET.get('chart', None)
    
    saat_ini = datetime.datetime.today()
    tahun_ini = saat_ini.strftime("%Y")

    direktorat_q = Pegawai.objects.values('direktorat').distinct()
    if tipe_chart == 'line':
        hasil = {}
        for k in direktorat_q:
            r,g,b = colorGen(k['direktorat'])
            hasil[k['direktorat']] = {}
            hasil[k['direktorat']]['label'] = k['direktorat']
            hasil[k['direktorat']]['data'] = []
            hasil[k['direktorat']]['borderColor'] = f'rgba({r},{g},{b}, 0.7)'
            hasil[k['direktorat']]['backgroundColor'] = hasil[k['direktorat']]['borderColor']
            hasil[k['direktorat']]['fill'] = False
        
        locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
        labels = []
        for i in range(5):
            waktu_s = saat_ini + datetime.timedelta(days=((i-2)*30))
            labels.append(waktu_s.strftime("%B %Y"))

            q_obj = Sertifikasi.objects.filter(akhir_berlaku__gt=waktu_s.date()).prefetch_related('pegawai')
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

    if tipe_chart == 'pie':
        labels = []
        data = []
        color = []
        q_obj = Sertifikasi.objects.filter(akhir_berlaku__gt=saat_ini.date()).prefetch_related('pegawai')
        count_q = q_obj.values('pegawai__direktorat').annotate(jumlah = Count('pegawai__direktorat'))
        for divisi in direktorat_q:
            labels.append(divisi['direktorat'])
            jumlah_q = count_q.filter(pegawai__direktorat=divisi['direktorat'])
            jumlah = 0
            if not jumlah_q.exists() : 
                jumlah = 0
            else : 
                jumlah = jumlah_q[0]['jumlah']
            data.append(jumlah)
            r,g,b = colorGen(divisi['direktorat'])
            color.append(f'rgba({r},{g},{b},1)')
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
            'color' : color
        })


            

