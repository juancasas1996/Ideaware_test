# Ideaware_test

Instrucciones de Ejecución del Sistema
Para ejecutar el sistema, sigue estos pasos:

1. Abre una terminal y navega hasta la carpeta Ideaware.
2. Crea un ambiente virtual con Conda o Virtualenv. Por ejemplo:

```
conda create --name mi_entorno_virtual python=3.10

```
3. Activa el ambiente virtual:
```
conda activate mi_entorno_virtual

```
4.Instala los paquetes necesarios utilizando pip:
```
conda activate mi_entorno_virtual

```
5.Navega hasta la carpeta Ideaware/mi_proyecto.
6.Inicia el servicio ejecutando el siguiente comando:

```
python manage.py runserver

```

Una vez que el servicio esté en funcionamiento, podrás acceder a él y utilizar las funcionalidades proporcionadas por los endpoints REST.

# Enviando Solicitudes a los Endpoints
### Cargar Documento .docx:
Para cargar un documento .docx a través del endpoint correspondiente, sigue estos pasos:

1.Abre una terminal y navega hasta la ruta donde se encuentra el documento .docx que deseas cargar.

```
curl -X POST -F "archivo_docx=@Test.docx" http://127.0.0.1:8000/cargar-docx/

```

Este comando enviará el documento .docx al endpoint cargar-docx, donde será procesado y almacenado.

# Búsqueda de Documentos
Para buscar documentos utilizando el endpoint correspondiente, sigue estos pasos:

1. Abre una terminal.
2. Ejecuta el siguiente comando curl, reemplazando "inteligencia artificial" con la query deseada:
   
```
curl -X POST -d "query=inteligencia artificial" http://127.0.0.1:8000/buscar-documentos/

```
Este comando enviara una solicitud REST al endpoint y este respondera con el documento con mayor similaridad a la query.
