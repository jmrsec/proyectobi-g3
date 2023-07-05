import tensorflow as tf
import numpy as np
from PIL import Image
from django.db.models import F
from .models import Usuario, ImagenUsuario
import io
from PIL import Image
from .loaded_model import load_model_once
import cv2

def obtenerUsuariosFotos(model):
    datos = Usuario.objects.select_related('imagenes').values('dni', 'nombre', 'apellido', 'imagenes__imagen')
    diccionarioUsuarios = {}

    for usuario in datos:
        if usuario['dni'] not in diccionarioUsuarios:
            diccionarioUsuarios[usuario['dni']] = {'nombre':usuario['nombre'],
                                                          'apellido':usuario['apellido'],
                                                          'fotos':[]}
        if usuario['imagenes__imagen'] != b'':
            img = usuario['imagenes__imagen']
            img = io.BytesIO(img)
            img = Image.open(img)
            img = img.resize((160, 160))
            vector = codificarImagen(img, model)
            diccionarioUsuarios[usuario['dni']]['fotos'].append(vector)
    return diccionarioUsuarios


def codificarImagen(imagen, model):

    imagen = np.around(np.array(imagen) / 255.0, decimals=12) # Valores del 0 al 1
    X = np.expand_dims(imagen, axis=0) # Aumenta la dimension de la imagen (1,160,160,3)
    embedding = model.predict_on_batch(X) # Vector identificador
    return embedding / np.linalg.norm(embedding, ord=2) # Vector (0 al 1)


def buscarBD(vector,database, score):
    minimo = 1000

    for (id, nvec) in database.items():
        dist = 1000
        if nvec['fotos'] != []:
            aux = np.concatenate(nvec['fotos'], axis=0)
            aux = np.mean(aux, axis=0)
            dist = np.linalg.norm((vector-aux))
        if dist < minimo:
            minimo = dist
            persona = database[id]
            persona['id'] = id
            persona['fotos'] = len(persona['fotos'])
    print(minimo)
    if minimo > 0.7 or score> 0.7:
        return False,None, minimo
    
    return True,persona, minimo

def recortar_cara(imagen):
    # Convertir la imagen a formato BGR (utilizado por OpenCV)
    imagen_bgr = cv2.cvtColor(np.array(imagen), cv2.COLOR_RGB2BGR)

    # Cargar el clasificador pre-entrenado para la detección de rostros
    cascada_cara = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Convertir la imagen a escala de grises
    gris = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en la imagen
    rostros = cascada_cara.detectMultiScale(gris, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Verificar si se detectó al menos un rostro
    if len(rostros) > 0:
        # Recorrer los rostros detectados y recortar la región de interés (ROI)
        for (x, y, w, h) in rostros:
            # Ampliar la región de interés (ROI)
            roi_x = max(0, x - int(w * 0.2))
            roi_y = max(0, y - int(h * 0.2))
            roi_w = min(imagen_bgr.shape[1] - roi_x, int(w * 1.4))
            roi_h = min(imagen_bgr.shape[0] - roi_y, int(h * 1.4))
            cara = imagen_bgr[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

        # Crear una nueva imagen PIL con la cara recortada
        cara_pil = Image.fromarray(cv2.cvtColor(cara, cv2.COLOR_BGR2RGB))
        return cara_pil
    else:
        # Si no se detectó ningún rostro, retorna None o realiza alguna acción apropiada en tu aplicación
        return imagen

def verificarImagenBD(imagen, scoreA):
    model = load_model_once()
    vectorI = codificarImagen(imagen, model)
    diccDatabase = obtenerUsuariosFotos(model)
    resultado, persona, score = buscarBD(vectorI,diccDatabase, scoreA)
    score = scoreA*0.15+score*0.85
    return resultado, persona, score