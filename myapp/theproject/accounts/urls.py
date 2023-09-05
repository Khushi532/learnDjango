from django.urls import path

from . import views

# URL Mapping
urlpatterns = [
    path('register',views.register,name="register"),
]