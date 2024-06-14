from django.urls import path,include
from .custome_views import default

urlpatterns = [
    path('',default.home),
    path('test',default.test),
]
