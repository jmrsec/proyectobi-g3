from nturl2path import url2pathname
from django.urls import path
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
    path('usuarios',views.usuarios, name='usuarios')
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)