from .views import *
from django.urls import path


urlpatterns = [
    path('',dashboard,name='dashboard'),
    path('profile',profile,name='profile'),
    path('generate-blog-topic',blogTopic,name='generate-blog-topic'),
    path('blog-Section',blogSection,name='blog-section'),

    
]
