from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from .models import Penyelenggara
from django.db.models import Q

from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

# Create your views here.
# Create your views here.
def penyelenggara_view(request, *args, **kwargs):
    return render(request, 'penyelenggara.html', {})

def tambah_penyelenggara(request, *args, **kwargs):
    if request.method == "POST":
        if 'penyelenggara' in request.POST:
            banyak_q = Penyelenggara.objects.all()
            banyak = banyak_q.count()
            kode = f"P{banyak+1:04d}"
            penyelenggara_str = request.POST.get('penyelenggara', None)
            msg = ''
            try:
                Penyelenggara.objects.create(
                    nama_penyelenggara=penyelenggara_str,
                    kode_penyelenggara=kode
                )
            except Exception as e:
                msg = 'Error memasukkan penyelenggara, mohon hubungi admin'
            if request.is_ajax():
                return JsonResponse(data={'msg':msg})
            return redirect('penyelenggara:daftar-penyelenggara')

        if len(request.FILES) != 0:
            excel_file = request.FILES["excel_file"]
            if (str(excel_file)).split('.')[-1] == "xls" :
                data = xls_get(excel_file)
            elif (str(excel_file)).split('.')[-1] == "xlsx" :
                data = xlsx_get(excel_file, column_limit=4)
            else:
                return redirect('daftar-penyelenggara')
            penyelenggara_s = data['Sheet1']
            if len(penyelenggara_s) > 1:
                key = []
                iter = 1
                for penyelenggara in penyelenggara_s:
                    if len(penyelenggara) > 0:
                        if(penyelenggara[0]!='penyelenggara'):
                            try:
                                filtered = Penyelenggara.objects.filter(nama_penyelenggara=penyelenggara[0])
                            except Exception as e:
                                print(e)
                            if filtered.count() == 0 :
                                try:
                                    Penyelenggara.objects.create(
                                        nama_penyelenggara = penyelenggara[0],
                                        kode_penyelenggara = f"P{iter:04d}",
                                    )
                                except Exception as e:
                                    print(f'{iter} {e} {penyelenggara[0]}')
                                finally:
                                    iter+=1
                return redirect('penyelenggara:daftar-penyelenggara')

class QueryJSON(BaseDatatableView):
    model = Penyelenggara
    columns = ['nomor','nama_penyelenggara', 'kode_penyelenggara']
    order_columns = ['nomor','nama_penyelenggara','kode_penyelenggara']
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