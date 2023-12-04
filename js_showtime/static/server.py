from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pathlib import Path

app = FastAPI()

# Sirve archivos estáticos desde la carpeta 'src'
app.mount("/static", StaticFiles(directory="src"), name="static")

@app.get("/assets/{file_path:path}")
async def get_glb(file_path: str):
    file_location = Path("src/assets") / Path(file_path)
    if file_location.exists() and file_location.suffix == ".obj":
        return FileResponse(file_location, media_type="model/obj-binary")
    return FileResponse(file_location)  # Puedes manejar archivos no encontrados o tipos de archivo incorrectos según sea necesario
