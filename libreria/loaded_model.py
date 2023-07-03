import tensorflow as tf

loaded_model = None
tokenSesion = 0

def load_model_once():
    global loaded_model
    if loaded_model is None:
        loaded_model = tf.keras.models.load_model('./keras-facenet_tf23')
    return loaded_model

def iniciarSesion():
    global tokenSesion
    tokenSesion = 123
    return

def cerrarSesion():
    global tokenSesion
    tokenSesion = 0
    return

def getToken():
    global tokenSesion
    return tokenSesion