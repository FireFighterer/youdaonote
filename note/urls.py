from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from . import views
urlpatterns=[
    url(r'^add_note',views.add_note),
    url(r'^list_note',views.list_note,name="list_note"),
    url(r'^modify_note/(\d+)',views.modify_note),
    url(r'^look_note/(\d+)',views.look_note),
    url(r'^delete_note/(\d+)',views.delete_note),
    url(r'^search_note/',views.search_note),
    url(r'^delete_accessory/(\d+)',views.delete_accessory),
    # url(r'^accessory',views.accessory),
]