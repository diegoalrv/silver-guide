from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

modules_path = "node_modules"

# Ruta absoluta de la carpeta que deseas montar
ruta_absoluta = os.path.join(Path(__file__).resolve().parent.parent, modules_path)

print(ruta_absoluta)

# Monta la carpeta
app.mount(f"/app/{modules_path}", StaticFiles(directory=f"/app/{modules_path}"), name=modules_path)
app.mount(f"/app", StaticFiles(directory='/app'), name="app")

@app.get("/")
async def serve_threjs_app():
    # Ruta local al archivo HTML de tu aplicación de Three.js
    app_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join("/app", "index.html")
    return FileResponse(html_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008)