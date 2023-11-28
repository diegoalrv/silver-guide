# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el script run.sh y requirements.txt al contenedor
COPY run.sh ./
COPY requirements.txt ./

# Hacer que run.sh sea ejecutable
RUN chmod +x run.sh

# Instalar las dependencias del archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar run.sh cuando se inicie el contenedor
CMD ["./run.sh"]
