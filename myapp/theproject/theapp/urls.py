from typing import Mapping
from django.urls import path

from . import views

# URL Mapping
urlpatterns = [
    path('',views.home,name="home"),
    path('add',views.add,name='add')
]