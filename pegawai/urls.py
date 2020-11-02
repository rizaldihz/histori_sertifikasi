from django.urls import path
from .views import *

app_name = 'pegawai'
urlpatterns = [
    path('',pegawai_view,name='daftar-pegawai'),
    # path('<str:dummy>-tr.<int:prid>', product_detail_view, name='product-detail'),
    path('tambah', pegawai_tambah, name='tambah-pegawai'),
    # path('create2', product_create_scratch_view, name='product-create-2'),
    # path('delete/<str:dummy>-<int:prid>', product_delete_view, name='product'),
]
