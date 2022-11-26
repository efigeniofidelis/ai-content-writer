from .views import *
from django.urls import path


urlpatterns = [
    path('',dashboard,name='dashboard'),
    path('profile',profile,name='profile'),
    path('delete-blog-topic/<str:uniqueId>/',deleteblogTopic,name='delete-blog-topic'),
    path('generate-blog-from-topic/<str:uniqueId>/',createBlogFromTopic,name='generate-blog-from-topic'),
    path('generate-blog-topic',blogTopic,name='generate-blog-topic'),
    path('blog-Section',blogSection,name='blog-section'),
# saving the blog topic for future use
    path('save-blog-topic/<str:blogTopic>/',saveBlogTopic,name='save-blog-topic'),
    path('use-blog-topic/<str:blogTopic>/',useBlogTopic,name='use-blog-topic'),
    path('view-generated-blog/<slug:slug>/',viewGeneratedBlog,name='view-generated-blog'),
#billing page

    path('billing',billing,name='billing'),
   # path('d5717186-3502-4378-8308-e2700382498b',webhook,name='webhook'),
]
