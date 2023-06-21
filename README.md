# PROYECTO G3

# INTEGRANTES
- Bernedo, Bruno
- Chumpitaz, Renzo
- Cisneros, Gloria
- Garay, Jeanpier
- Guillen, Ritcy
- Machare, Jeremy
- Villafranca, Patrick

# INSTALACIÓN

> Para ejecutar el proyecto es necesario instalar python 3.10.x y pip

Clonamos el repositorio:
```sh
git clone https://github.com/Jeremymr2/proyectobi-g3.git
```

Instalamos la librería de virtualenv:
```sh
pip install virtualenv
```

Creamos el entorno virtual:
```sh
python -m virtualenv
```

Activamos el entorno virtual:
```sh
.\env\Scripts\activate
```

> En caso usemos windows y nos salga el error de activación, usar:
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Procedemos con la instalación de paquetes:
```sh
pip install -r requirements.txt
```

Ahora iniciamos con la migración de la bd:

> Para ello es necesario tener mysql instalado

Crearemos una base de datos en mysql mediante la query:
```sql
CREATE DATABASE libreria_g3;
```

Editamos los datos del archivo `settings.py`, con las credenciales de nuestro mysql:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'libreria_g3',
        'USER': 'Usuario',
        'PASSWORD': 'Contraseña',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

Procederemos con la migración. Abrimos una consola de comandos e ingresamos:

``` sh
python manage.py migrate
```

Luego ejecutamos la página:
```sh
python manage.py runserver
```

Abrimos el siguiente link: `localhost:8000`