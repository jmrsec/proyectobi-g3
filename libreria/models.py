from tabnanny import verbose
from django.db import models

# Create your models here.
class Libro(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, verbose_name = "Titulo")
    imagen = models.ImageField(upload_to='imagenes/',verbose_name = "Imagen" ,null=True)
    descripcion = models.TextField(verbose_name = "Descripcion", null=True)
    publicacion = models.DateField(verbose_name = "Publicacion",null=True)
    autor = models.TextField(verbose_name = "Autor",null=True)

    def __str__(self):
        fila = "Titulo: " + self.titulo + " - " + "Descripcion: " + self.descripcion
        return fila