from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('camellia_input', views.camellia_input, name="camellia_input"),
    path('camellia', views.camellia, name="camellia"),
    path('chacha20_input', views.chacha20_input, name="chacha20_input"),
    path('chacha20', views.chacha20, name="chacha20"),
    path('kuznyechik_input', views.kuznyechik_input, name="kuznyechik_input"),
    path('kuznyechik', views.kuznyechik, name="kuznyechik")
]