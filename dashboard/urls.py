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
#product names

    path('product_names',productTopic,name='product_names'),
    path('show_names',show_names,name='show_names'),


#product ads

    path('product_ads',generate_ads,name='product_ads'),
    path('show_product_ads',show_ads,name='show_product_ads'),

#text to keyword

    path('text_to_keyword',extract_keywords,name='text_to_keyword'),
    path('show_text_to_keyword',show_keywords,name='show_text_to_keyword'),

#extraxt contact info

    path('contact_info',contact_info,name='contact_info'),
    path('show_contact',show_contact,name='show_contact'),

#study notes

    path('generate_study_notes',generate_study_notes,name='generate_study_notes'),
    path('show_study_notes',show_study_notes,name='show_study_notes'),
#billing page


    path('billing',billing,name='billing'),
   # path('d5717186-3502-4378-8308-e2700382498b',webhook,name='webhook'),
]
