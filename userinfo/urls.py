from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from . import  views
urlpatterns = [
     url(r'^login', views.mylogin),
     url(r'^reg', views.register),
     url(r'^logout', views.mylogout),

]