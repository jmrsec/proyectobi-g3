from django.contrib import admin
from .models import Libro
from .models import Usuario
from .models import ImagenUsuario

# Register your models here.
admin.site.register(Libro)
admin.site.register(Usuario)
admin.site.register(ImagenUsuario)