
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

 
urlpatterns = [ 
    path('mazamamedia_chatbotapi/', index, name='index'),       
    path('submit_info/<str:id>', submit_info, name='submit_info'),
    path('start/<str:user_id>/', disclosure,name = "disclosure"),
    path('post/',post_entry),
    path('submit_form/',submit_form, name="submit_form"),
     
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

