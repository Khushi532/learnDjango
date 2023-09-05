from django.urls import path

from . import views

# URL Mapping
urlpatterns = [
    path('',views.cal_sd,name="cal_sd"),
]