"""histori_sertif URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from sertifikasi.views import beranda_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sertifikasi/', include('sertifikasi.urls')),
    path('penyelenggara/', include('penyelenggara.urls')),
    path('skema/', include('skema.urls')),
    path('pegawai/', include('pegawai.urls')),
    path('bidang/', include('bidang.urls')),
    path('laporan/', include('laporan.urls')),
    path('', beranda_view, name='beranda')
]
