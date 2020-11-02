from django.urls import path
from .views import *

app_name = 'bidang'
urlpatterns = [
    path('',bidang_view, name='daftar-bidang'),
    # path('<str:dummy>-tr.<int:prid>', product_detail_view, name='product-detail'),
    path('tambah', tambah_bidang, name='tambah-bidang'),
    # path('create2', product_create_scratch_view, name='product-create-2'),
    # path('delete/<str:dummy>-<int:prid>', product_delete_view, name='product'),
    path('data',QueryJSON.as_view(), name='query-bidang'),
]
