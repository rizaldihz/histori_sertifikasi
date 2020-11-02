from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from .models import Skema

from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

def skema_view(request, *args, **kwargs):
    return render(request, 'skema.html', {})

def tambah_skema(request, *args, **kwargs):
    if 'skema' in request.POST:
        banyak_q = Skema.objects.all()
        banyak = banyak_q.count()
        kode = f"S{banyak+1:04d}"
        skema_str = request.POST.get('skema', None)
        msg = ''
        try:
            Skema.objects.create(
                nama_skema=skema_str,
                kode_skema=kode
            )
        except Exception as e:
            msg = 'Error memasukkan skema, mohon hubungi admin'
        if request.is_ajax():
            return JsonResponse(data={'msg':msg})
        return redirect('skema:daftar-skema')
    if request.method == "POST":
        if len(request.FILES) != 0:
            excel_file = request.FILES["excel_file"]
            if (str(excel_file)).split('.')[-1] == "xls" :
                data = xls_get(excel_file)
            elif (str(excel_file)).split('.')[-1] == "xlsx" :
                data = xlsx_get(excel_file, column_limit=4)
            else:
                return redirect('daftar-skema')
            skema_s = data['Sheet1']
            if len(skema_s) > 1:
                key = []
                iter = 1
                for skema in skema_s:
                    if len(skema) > 0:
                        if(skema[0]!='Skema (BNSP)'):
                            try:
                                filtered = Skema.objects.filter(nama_skema=skema[0])
                            except Exception as e:
                                print(e)
                            if filtered.count() == 0 :
                                try:
                                    Skema.objects.create(
                                        nama_skema = skema[0],
                                        kode_skema = f"S{iter:04d}",
                                    )
                                except Exception as e:
                                    print(f'{iter} {e} {skema[0]}')
                                finally:
                                    iter+=1
                return redirect('skema:daftar-skema')

class QueryJSON(BaseDatatableView):
    model = Skema
    columns = ['nomor','nama_skema', 'kode_skema']
    order_columns = ['nomor','nama_skema','kode_skema']
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