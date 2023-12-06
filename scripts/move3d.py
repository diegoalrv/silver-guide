import pyvista as pv
import time

# Crear el plotter
plotter = pv.Plotter()

# Crear tres cajas con alturas diferentes
cajas = {
    'caja1': pv.Box(bounds=(-1, 1, -1, 1, 0, 2)),
    'caja2': pv.Box(bounds=(-3, -1, -1, 1, 0, 3)),
    'caja3': pv.Box(bounds=(1, 3, -1, 1, 0, 4))
}

# Añadir las cajas al plotter
for id, caja in cajas.items():
    plotter.add_mesh(caja, name=id)

# Crear un plano que actúe como el piso
piso = pv.Plane(center=(0, 0, 0), direction=(0, 0, 1), i_size=10, j_size=10)
plotter.add_mesh(piso, color='green')

# Función para mover un objeto en el eje Z
def move_object_z(id, delta_z):
    caja = cajas[id].copy()  # Crear una copia de la malla
    caja.translate((0, 0, delta_z))
    plotter.remove_actor(plotter.actors[id])  # Remover el actor anterior
    plotter.add_mesh(caja, name=id)  # Añadir la malla actualizada

# Mover las cajas hacia arriba y luego hacia abajo
plotter.show(interactive_update=True)  # Abre la ventana de visualización
# plotter.update()
for a in range(10):  # Subir 10 unidades
    print(a)
    for id in cajas:
        move_object_z(id, 10)
        # plotter.update()
        plotter.render()
        plotter.update(stime=10)
    time.sleep(0.5)  # Añadir un retraso

for b in range(10):  # Bajar 10 unidades
    print(b)
    for id in cajas:
        move_object_z(id, -10)
        # plotter.update()
        plotter.render()
        plotter.update(stime=10)
    time.sleep(0.5)  # Añadir un retraso

plotter.close()  # Cierra la ventana de visualización
