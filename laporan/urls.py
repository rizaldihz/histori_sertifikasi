from django.urls import path
from .views import *

app_name = 'laporan'
urlpatterns = [
    path('grafik',grafik_view,name='daftar-grafik'),
    path('pivot',pivot_view,name='daftar-pivot'),
    # path('<str:dummy>-tr.<int:prid>', product_detail_view, name='product-detail'),
    # path('create2', product_create_scratch_view, name='product-create-2'),
    # path('delete/<str:dummy>-<int:prid>', product_delete_view, name='product'),
    path('data', QueryJSON.as_view(), name='query-laporan'),
    path('chart-data', chartQuery, name='chart-query-laporan'),
    path('filter-chart', chartQuery, name='filter-laporan-grafik')
]
