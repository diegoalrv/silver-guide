from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import base64
import os
import json

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origins
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

# Monta la carpeta "static" en el directorio raíz
app.mount("/src", StaticFiles(directory="src"), name="src")

@app.get("/")
async def read_root():
    return FileResponse("src/index.html")

@app.get("/hello")
async def hello_world():
    return {'hello': 'miaaaaaaau'}

class ImageData(BaseModel):
    image: str
    droneData: dict

@app.post("/upload_image_from_drone")
async def upload_image_from_drone(data: ImageData):
    try:
        timestamp = data.droneData['timestamp']
        image_filename = f'./imgs/{timestamp}.png'
        data_filename = f'./data/{timestamp}.json'

        # Crear directorios si no existen
        os.makedirs(os.path.dirname(image_filename), exist_ok=True)
        os.makedirs(os.path.dirname(data_filename), exist_ok=True)

        # Guardar la imagen
        image_data = base64.b64decode(data.image.split(',')[1])
        with open(image_filename, "wb") as file:
            file.write(image_data)

        # Guardar los datos del dron
        with open(data_filename, "w") as file:
            json.dump(data.droneData, file)

        return {"message": "Imagen y datos del dron guardados correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
