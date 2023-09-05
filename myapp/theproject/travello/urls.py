from django.urls import path

from . import views

# URL Mapping
urlpatterns = [
    path('',views.index,name="index"),
]