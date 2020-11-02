from django.shortcuts import render, redirect
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from .models import Pegawai
from django.contrib.auth.models import User

# Create your views here.
def pegawai_view(request, *args, **kwargs):
    
    return render(request, 'pegawai.html', {})

def pegawai_tambah(request, *args, **kwargs):
    if request.method == "POST":
        if len(request.FILES) != 0:
            excel_file = request.FILES["excel_file"]
            if (str(excel_file)).split('.')[-1] == "xls" :
                data = xls_get(excel_file)
            elif (str(excel_file)).split('.')[-1] == "xlsx" :
                data = xlsx_get(excel_file, column_limit=4)
            else:
                return redirect('daftar-pegawai')
            pegawai_s = data['datapegawaiaktif']    
            if len(pegawai_s) > 1:
                key = []
                iter = 1
                for pegawai in pegawai_s:
                    if len(pegawai) > 0:
                        if(pegawai[0] == 'nik'):
                            key = pegawai
                        elif(pegawai[0]!='nik'):
                            filtered = Pegawai.objects.filter(nik=pegawai[0])
                            if filtered.count() == 0 :
                                try:
                                    Pegawai.objects.create(
                                        nik = pegawai[0],
                                        nik_sap = pegawai[1],
                                        nama = pegawai[2],
                                        p_grade = pegawai[3],
                                        job_grade = pegawai[4],
                                        grade_sap = pegawai[5],
                                        nama_jabatan = pegawai[6],
                                        jabatan = pegawai[7],
                                        kode_unitkerja = pegawai[8],
                                        kode_dir = pegawai[9],
                                        kode_komp = pegawai[10],
                                        kode_dept = pegawai[11],
                                        kode_bagian = pegawai[12],
                                        kode_seksi = pegawai[13],
                                        direktorat = pegawai[14],
                                        kompartemen = pegawai[15],
                                        departemen = pegawai[16],
                                        bagian = pegawai[17],
                                        seksi = pegawai[18],
                                        regu = pegawai[19],
                                        poscode = pegawai[20],
                                        postitle = pegawai[21],
                                        alamat = pegawai[22],
                                        kelurahan = pegawai[23],
                                        kecamatan = pegawai[24],
                                        kabupaten = pegawai[25],
                                        provinsi = pegawai[26],
                                        kode_pos = pegawai[27],
                                        lp = pegawai[28],
                                        nik_bp = pegawai[29],
                                        akses_sistem = '0'
                                    )
                                    try:
                                        User.objects.create_user(username=pegawai[0],password=pegawai[0])
                                    except Exception as e:
                                        print(e)
                                        # pass
                                except Exception as e:
                                    print(f'{iter} {e} {pegawai[2]}')
                    iter+=1
                return redirect('pegawai:daftar-pegawai')


