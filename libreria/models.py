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
    
class Usuario(models.Model):
    dni = models.CharField(primary_key=True,max_length=8)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.dni}: {self.nombre} {self.apellido}"
    
class ImagenUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.BinaryField()

    def __str__(self):
        return f"Imagen {self.id} - {self.usuario.nombre} {self.usuario.apellido}"