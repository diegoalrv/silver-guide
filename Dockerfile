# Usar una imagen base de Ubuntu
FROM ubuntu:latest

# Actualizar el sistema e instalar las dependencias necesarias
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-opengl
RUN apt-get install -y python3-pygame
# Instalar X11 sin interacción
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y xorg
# Habilitar soporte OpenGL en X11
RUN apt-get install -y mesa-utils
# Instalar xauth en el contenedor
RUN apt-get install -y xauth
# Instalar bibliotecas Python adicionales según sea necesario
RUN pip3 install pandas shapely geopandas numpy matplotlib pyvista

# Establecer la variable de entorno XAUTHORITY
ENV XAUTHORITY /root/.Xauthority
# Habilitar soporte OpenGL
ENV LIBGL_ALWAYS_INDIRECT 1
# Establecer variables de entorno para X11
ENV DISPLAY=:0

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar tus archivos de Python y datos al contenedor
COPY app.py /app/
# COPY tus_datos_georeferenciados /app/tus_datos_georeferenciados/

# Ejecutar tu script cuando se inicie el contenedor
CMD ["python3", "app.py"]
