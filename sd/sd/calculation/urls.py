from django.urls import path

from . import views

# URL Mapping
urlpatterns = [
    path('calculate',views.calculate,name="calculate"),
]

