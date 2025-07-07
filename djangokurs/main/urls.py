
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name = 'index'),
    path('search',views.search,name = 'search'),
    path('contact/', views.contact, name='contact'),
    path('kategori/<slug:slug>',views.getCategories,name = 'getCategories'),
    path('course/<slug:slug>',views.getCourses,name = 'getCourses'),
    path('kurs-ekle/',views.KursEkle,name = 'kursEkle'),
    path('icerik/<int:id>',views.icerik,name = 'icerik')
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

