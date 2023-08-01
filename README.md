# Render All!

Este es un simple renderizardor en cola para archivos de Nuke (.nk).

### Installation:
-Descarga el archivo .zip para tu sistema operativo (Windows o Linux)

  https://drive.google.com/drive/folders/1io6Bzk6VWzec3zipq8IImg4PL-oegFce?usp=drive_link

-Descomprime el zip y abre el archivo ejecutable (Render all)

### Usage:
Follow these steps to use it:
1. Setea la ruta del archivo ejecutable de Nuke, por defecto para Windows es 'C:\Program Files\Nuke14.0v4\Nuke14.0.exe'
2. Escribe el nombre exacto del nodo Write que quieres renderizar, debe ser el mismo nombre para todos los scripts, es recomendable usar una nomencaltura standard para nombrar a los nodos Write (por defecto renderizará el 'Write1').
3. Agrega y quita archivos de la cola de render, hay tres formas de agregar nuevos archivos:
   
    a) Arrastrando los scripts 

    b) Con boton ´+´ para abrir un buscador de archivos

    c) Usando una base de datos, esta funcion aun no esta disponible (Ya estoy trabajando en un plugin para cargar scripts a la base de datos desde nuke)


5. Opcionalmente hay dos funciones para habilitar con un checkbox:
   
    a) Abrir la carpeta que contiene los render terminados cada vez que finalice cada render

    b) Apagar el equipo automaticamente 10 minutos despues de finalizar toda la cola de render

5. Click Render! Ejecutara el comando para renderizar todos los archivos de la cola. Puedes detener el render en cualquier momento, esto eliminará el proceso.

### Notes on Possible Errors:
There might also be conflicts with Linux (Not tested), I cant make a macOs version, I will try to do it soon.
Espero que sea de ayuda, se agradece cualquier reporte de error.


