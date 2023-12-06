import bpy
import sys
import os

# Obtener argumentos de la línea de comandos
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # obtener todos los args después de "--"

# Ruta del archivo .obj
obj_file = argv[0]

# Ruta del archivo .gltf de salida
gltf_file = os.path.splitext(obj_file)[0] + ".gltf"

# Cargar el archivo .obj
bpy.ops.import_scene.obj(filepath=obj_file)

# Exportar a .gltf
bpy.ops.export_scene.gltf(filepath=gltf_file)
