from .views import *
from django.urls import path


urlpatterns = [
    path('',dashboard,name='dashboard'),
    
]
