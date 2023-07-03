from nturl2path import url2pathname
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('',views.inicio, name='inicio'),
    path('nosotros',views.nosotros, name='nosotros'),
    path('libros',views.libros, name='libros'),
    path('libros/editar',views.editar, name='editar'),
    path('eliminar/<int:id>',views.eliminar, name='eliminar'),
    path('libros/editar/<int:id>',views.editar, name='editar'),
    path('usuarios',views.usuarios, name='usuarios'),
    path('usuarios/editar',views.editar_usuario, name='editar_usuario'),
    path('usuarios/editar/<str:dni>',views.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<str:dni>',views.eliminar_usuario, name='eliminar_usuario'),
    #path('eliminar/<int:id>',views.eliminar_usuario, name='eliminar_usuario'),
    path('imagenes',views.imagenes, name='imagenes'),
    #path('eliminar/<int:id>',views.eliminar_imagen, name='eliminar_imagen'),
    #path('', views.inicio, name='index'),
    path('login/', views.login, name='login')

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)