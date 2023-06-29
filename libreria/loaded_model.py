import tensorflow as tf

loaded_model = None

def load_model_once():
    global loaded_model
    if loaded_model is None:
        loaded_model = tf.keras.models.load_model('./keras-facenet_tf23')
    return loaded_model