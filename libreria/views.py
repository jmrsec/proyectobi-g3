from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Libro
from .models import Usuario
from .models import ImagenUsuario
from .forms import LibroForm
from .forms import UsuarioForm
from PIL import Image
import base64
import io
from .modelFR import recortar_cara
from .modelFR import verificarImagenBD
# Create your views here.

@login_required
def inicio(request):
    return render(request, 'vistas/inicio.html')

@login_required
def nosotros(request):
    return render(request, 'nosotros/nosotros.html')

@login_required
def usuarios(request):
    usuarios = Usuario.objects.all()
    imagenes = []
    for user in usuarios:
        imagenbin = ImagenUsuario.objects.filter(usuario_id=user.dni).last().imagen
        imagenbin = io.BytesIO(imagenbin)
        imagenbin = Image.open(imagenbin)
        imagenbin = imagenbin.resize((40, 40))
        with io.BytesIO() as buffer:
            imagenbin.save(buffer, format="JPEG")
            imagenes.append(base64.b64encode(buffer.getvalue()).decode("utf-8"))
    formulario = UsuarioForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        dni = formulario.cleaned_data['dni']
        nombre = formulario.cleaned_data['nombre']
        apellido = formulario.cleaned_data['apellido']
        imagen = request.FILES['imagen']
        usuario = (dni,nombre,apellido)
        nuevoUsuario = Usuario(dni=dni,nombre=nombre,apellido=apellido)
        # Transforma binario a jpg
        # Abrir la imagen utilizando PIL
        imagen_pil = Image.open(imagen)
        imagen_pil = recortar_cara(imagen_pil)
        # Guarda el usuario en la tabla Usuario
        nuevoUsuario.save()
        # Convertir la imagen a bytes
        stream = io.BytesIO()
        imagen_pil.save(stream, format='JPEG')
        datos_binarios = stream.getvalue()
        imagen_usuario = ImagenUsuario(usuario=nuevoUsuario, imagen=datos_binarios)
        # Guardar el objeto del modelo en la tabla de ImagenUsuario de la base de datos
        imagen_usuario.save()
        return redirect('usuarios')
    return render(request, 'usuarios/index.html', {'usuarios': usuarios,'imagenes': imagenes, 'formulario': formulario})

@login_required
def editar_usuario(request,dni):
    usuario = Usuario.objects.get(dni=dni)
    formulario = UsuarioForm(request.POST or None, request.FILES or None, instance=usuario)
    if formulario.is_valid() and request.POST:
        dni = formulario.cleaned_data['dni']
        nombre = formulario.cleaned_data['nombre']
        apellido = formulario.cleaned_data['apellido']
        imagen = request.FILES['imagen']
        usuario = (dni,nombre,apellido)
        actualUsuario = Usuario(dni=dni,nombre=nombre,apellido=apellido)
        # Transforma binario a jpg
        # Abrir la imagen utilizando PIL
        imagen_pil = Image.open(imagen)
        imagen_pil = recortar_cara(imagen_pil)
        # Guarda el usuario en la tabla Usuario
        actualUsuario.save()
        # Convertir la imagen a bytes
        stream = io.BytesIO()
        imagen_pil.save(stream, format='JPEG')
        datos_binarios = stream.getvalue()
        imagen_usuario = ImagenUsuario(usuario=actualUsuario, imagen=datos_binarios)
        # Guardar el objeto del modelo en la tabla de ImagenUsuario de la base de datos
        imagen_usuario.save()
        return redirect('usuarios')
    return render(request, 'usuarios/editar.html', {'formulario': formulario})

@login_required
def eliminar_usuario(request,dni):
    imagen = ImagenUsuario.objects.filter(usuario_id=dni)
    imagen.delete()
    usuario = Usuario.objects.get(dni=dni)
    usuario.delete()
    return redirect('usuarios')

@login_required
def imagenes(request):
    imagenes = ImagenUsuario.objects.all()
    formulario = UsuarioForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('usuarios')
    return render(request, 'usuarios/index.html', {'usuarios': usuarios, 'formulario': formulario})

@login_required
def eliminar_imagen(request,dni):
    imagen = ImagenUsuario.objects.get(usuario_id=dni)
    imagen.delete()
    return redirect('usuarios')

@login_required
def libros(request):
    libros = Libro.objects.all()
    formulario = LibroForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('libros')
    return render(request, 'libros/index.html', {'libros': libros, 'formulario': formulario})

@login_required
def editar(request,id):
    libro = Libro.objects.get(id=id)
    formulario = LibroForm(request.POST or None, request.FILES or None, instance=libro)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('libros')
    return render(request, 'libros/editar.html', {'formulario': formulario})

@login_required
def eliminar(request,id):
    libro = Libro.objects.get(id=id)
    libro.delete()
    return redirect('libros')

def login(request):
    scoreInden = 0
    if request.method == 'POST':

        bandera = False
        usuario = {}

        image_data = request.POST.get('image_data', '')
        score = float(request.POST.get('score'))

        image_data = image_data.replace("data:image/jpeg;base64,", "")
        image_data = base64.b64decode(image_data)
        if image_data != b'':
            image = Image.open(io.BytesIO(image_data))
            image = recortar_cara(image)
            image = image.resize((160, 160))
            bandera, usuario, scoreInden = verificarImagenBD(image,score)


        return JsonResponse({'success': bandera, 'usuario':usuario, 'Score':scoreInden})
    
    return render(request, 'login.html')