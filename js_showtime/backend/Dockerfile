# Usar una imagen base de Python
FROM python:3.8-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos del proyecto al directorio de trabajo
COPY . /app

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que utiliza Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
