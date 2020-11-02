from django.urls import path
from .views import *

app_name = 'skema'
urlpatterns = [
    path('',skema_view,name='daftar-skema'),
    # path('<str:dummy>-tr.<int:prid>', product_detail_view, name='product-detail'),
    path('tambah', tambah_skema, name='tambah-skema'),
    # path('create2', product_create_scratch_view, name='product-create-2'),
    # path('delete/<str:dummy>-<int:prid>', product_delete_view, name='product'),
    path('data',QueryJSON.as_view(), name='query-skema'),
]
