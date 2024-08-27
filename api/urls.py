from myapp.views import index
from django.urls import path

urlpatterns = [
    path("index/", index),
]