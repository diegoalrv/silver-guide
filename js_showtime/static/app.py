from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

# Monta la carpeta "static" en el directorio raíz
app.mount("/static", StaticFiles(directory="src"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("src/index.html")

@app.get("/hello")
async def hello_world():
    return {'hello': 'miaaaaaaau'}
