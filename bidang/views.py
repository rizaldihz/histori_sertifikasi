from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from .models import Bidang
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get

from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

def bidang_view(request, *args, **kwargs):
    return render(request, 'bidang.html', {})

def tambah_bidang(request, *args, **kwargs):
    if 'bidang' in request.POST:
        banyak_q = Bidang.objects.all()
        banyak = banyak_q.count()
        kode = f"B{banyak+1:04d}"
        bidang_str = request.POST.get('bidang', None)
        msg = ''
        try:
            Bidang.objects.create(
                nama_bidang=bidang_str,
                kode_bidang=kode
            )
        except Exception as e:
            msg = 'Error memasukkan bidang, mohon hubungi admin'
        if request.is_ajax():
            return JsonResponse(data={'msg':msg})
        return redirect('bidang:daftar-bidang')

    if request.method == "POST":
        if len(request.FILES) != 0:
            excel_file = request.FILES["excel_file"]
            if (str(excel_file)).split('.')[-1] == "xls" :
                data = xls_get(excel_file)
            elif (str(excel_file)).split('.')[-1] == "xlsx" :
                data = xlsx_get(excel_file, column_limit=4)
            else:
                return redirect('daftar-bidang')
            bidang_s = data['Sheet1']
            if len(bidang_s) > 1:
                key = []
                iter = 1
                for bidang in bidang_s:
                    if len(bidang) > 0:
                        if(bidang[0]!='Bidang (BNSP)'):
                            try:
                                filtered = Bidang.objects.filter(nama_bidang=bidang[0])
                            except Exception as e:
                                print(e)
                            if filtered.count() == 0 :
                                try:
                                    Bidang.objects.create(
                                        nama_bidang = bidang[0],
                                        kode_bidang = f"B{iter:04d}",
                                    )
                                except Exception as e:
                                    print(f'{iter} {e} {bidang[0]}')
                                finally:
                                    iter+=1
                return redirect('bidang:daftar-bidang')

class QueryJSON(BaseDatatableView):
    model = Bidang
    columns = ['nomor','nama_bidang', 'kode_bidang']
    order_columns = ['nomor','nama_bidang','kode_bidang']
    max_display_length = 200

    def render_column(self, row, column):
        # # We want to render user as a custom column
        # if column == 'user':
        #     # escape HTML for security reasons
        #     return escape('{0} {1}'.format(row.customer_firstname, row.customer_lastname))
        # else:
        #     return super(OrderListJson, self).render_column(row, column)
        # # default customization
        return super(QueryJSON, self).render_column(row, column)