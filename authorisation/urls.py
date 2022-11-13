from .views import *
from django.urls import path


urlpatterns = [
    path('login', login,name='login'),
    path('signup',signup,name='signup'),
    path('logout',logout,name='logout'),
    
]
