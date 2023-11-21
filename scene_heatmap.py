# Importando PyVista y otras bibliotecas necesarias
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import geopandas as gpd
import pyvista as pv
from shapely.geometry import Polygon
from shapely.affinity import scale
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

def save_grid_as_texture(grid_gdf, output_filename="heatmap.png"):
    """
    Guarda el grid_gdf como una imagen de textura en el archivo especificado.

    :param grid_gdf: GeoDataFrame que contiene la geometría y los valores numéricos.
    :param output_filename: Nombre del archivo de imagen a guardar.
    """
    # Asumiendo que la columna numérica se llama 'num'
    column = 'num'

    # Determinar los límites del grid
    x_min, x_max = grid_gdf.bounds.minx.min(), grid_gdf.bounds.maxx.max()
    y_min, y_max = grid_gdf.bounds.miny.min(), grid_gdf.bounds.maxy.max()
    cell_size = (grid_gdf.geometry[0].bounds[2] - grid_gdf.geometry[0].bounds[0])  # Tamaño de una celda

    # Crear un mapa de colores de rojo a verde
    min_num = grid_gdf[column].min()
    max_num = grid_gdf[column].max()
    cmap = plt.cm.RdYlGn  # Red-Yellow-Green colormap

    # Dimensiones de la imagen de la textura
    num_x_cells = int((x_max - x_min) / cell_size)
    num_y_cells = int((y_max - y_min) / cell_size)
    texture_img = np.zeros((num_y_cells, num_x_cells, 3))  # Imagen RGB

    # Rellenar la imagen con los colores del grid
    for _, row in grid_gdf.iterrows():
        x_idx = int((row['geometry'].centroid.x - x_min) / cell_size)
        y_idx = int((row['geometry'].centroid.y - y_min) / cell_size)
        norm_value = (row[column] - min_num) / (max_num - min_num)
        color = cmap(norm_value)[:3]  # Obtener color del mapa de colores
        texture_img[y_idx, x_idx, :] = color

    # Guardar la imagen de la textura
    plt.imsave(output_filename, texture_img)


def create_grid(x_min, x_max, y_min, y_max, cell_size):
    """
    Crea una malla de cuadrados dentro de un cuadrado más grande.

    :param x_min: Mínimo valor de x del cuadrado grande.
    :param x_max: Máximo valor de x del cuadrado grande.
    :param y_min: Mínimo valor de y del cuadrado grande.
    :param y_max: Máximo valor de y del cuadrado grande.
    :param cell_size: Tamaño de cada cuadrado de la malla.
    :return: GeoDataFrame con la malla de cuadrados y sus valores numéricos.
    """
    # Crear cuadrados pequeños en la malla
    x_values = np.arange(x_min, x_max, cell_size)
    y_values = np.arange(y_min, y_max, cell_size)

    # Lista para almacenar los datos del GeoDataFrame
    data = []

    # Generar la malla de cuadrados y calcular 'num'
    for x in x_values:
        for y in y_values:
            # Crear un cuadrado pequeño
            square = Polygon([(x, y), (x + cell_size, y), (x + cell_size, y + cell_size), (x, y + cell_size)])
            
            # Calcular el centro del cuadrado
            center_x, center_y = x + cell_size / 2, y + cell_size / 2
            
            # Calcular 'num' como x^2 + y^2
            num = center_x**2 + center_y**2

            # Añadir al diccionario de datos
            data.append({'geometry': square, 'num': num})

    # Crear un GeoDataFrame
    return gpd.GeoDataFrame(data)

def create_prism_mesh_and_sides(polygon, height, h0=0):
    # Extraer los puntos x, y del polígono
    x, y = polygon.exterior.coords.xy

    # Crear los puntos para las caras superiores e inferiores
    top_points = [(xi, yi, height+h0) for xi, yi in zip(x, y)]
    bottom_points = [(xi, yi, h0) for xi, yi in zip(x, y)]

    # Combinar los puntos en una lista
    points = bottom_points[:-1] + top_points[:-1]

    # Calcular el número de puntos en el polígono
    num_points = len(polygon.exterior.coords) - 1

    # Crear las caras de la malla
    faces = [
        [num_points] + list(range(num_points)),             # Cara inferior
        [num_points] + list(range(num_points, 2 * num_points))  # Cara superior
    ]

    # Crear la malla principal del prisma
    main_mesh = pv.PolyData(points, faces)
    main_mesh.texture_map_to_plane(inplace=True)

    # Lista para guardar las mallas de las caras laterales
    side_meshes = []

    # Crear mallas para cada cara lateral
    for i in range(num_points):
        side_points = [
            points[i], points[(i + 1) % num_points],
            points[(i + 1) % num_points + num_points], points[i + num_points]
        ]
        side_faces = [[4, 0, 1, 2, 3]]  # Un cuadrilátero por cada cara lateral
        side_mesh = pv.PolyData(side_points, side_faces)

        # Asignar coordenadas de textura
        side_mesh.texture_map_to_plane(inplace=True)

        side_meshes.append(side_mesh)

    return main_mesh, side_meshes

def create_flat_mesh(polygon, h0=0):
    """Crea una malla plana a partir de un polígono."""
    x, y = polygon.exterior.coords.xy

    # Crear puntos para la malla plana
    points = [(xi, yi, h0) for xi, yi in zip(x, y)]

    # Crear la malla
    mesh = pv.PolyData(points, [[len(x) - 1] + list(range(len(x) - 1))])
    mesh.texture_map_to_plane(inplace=True)

    return mesh

def create_roof_shape(polygon, base_height, expansion_factor=1.03, roof_height_factor=0.25):
    """
    Crea una malla de techo para un polígono.

    :param polygon: Polígono base (shapely.geometry.Polygon).
    :param base_height: Altura de la base sobre la que se colocará el techo.
    :param expansion_factor: Factor de expansión para el tamaño del polígono.
    :param roof_height_factor: Factor para calcular la altura del techo a partir de las dimensiones del polígono.
    :return: Malla de techo (pyvista.PolyData).
    """
    # Calcular el centro del polígono y escalarlo
    center = polygon.centroid
    scaled_polygon = scale(polygon, xfact=expansion_factor, yfact=expansion_factor, origin=center)

    # Obtener puntos para la base del techo
    x, y = scaled_polygon.exterior.coords.xy
    base_points = [(xi, yi, base_height) for xi, yi in zip(x, y)]

    # Calcular un punto central superior para el techo
    roof_height = polygon.area ** 0.5 * roof_height_factor
    top_center = (center.x, center.y, base_height + roof_height)

    # Crear puntos y caras para el techo
    points = base_points[:-1]  # Excluir el último punto duplicado
    points.append(top_center)  # Añadir el punto central superior

    # Caras del techo (triángulos desde el punto central a la base)
    num_base_points = len(base_points) - 1
    faces = [[3, i, (i + 1) % num_base_points, num_base_points] for i in range(num_base_points)]

    # Crear la malla del techo
    roof_mesh = pv.PolyData(points, faces)
    roof_mesh.texture_map_to_plane(inplace=True)
    return roof_mesh


def main():

    # Crear un GeoDataFrame con el polígono cuadrado
    data = {
        'Id': [0, 1, 2],
        'Height': [5, 3, 0],
        'geometry':
            [
                Polygon([(0, 0), (0, 1), (1.5, 1), (1.5, 1.5), (1, 1.5), (1, 0), (0, 0)]),
                Polygon([(2, 0), (2, 1), (2, 1.5), (1, 1.5), (1, 0), (2, 0)]),
                Polygon([(-4,4), (-4, -4), (4, -4), (4, 4)]),
            ],
        }
    gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

    # Supongamos que ya tienes tu grid_gdf creado
    grid_gdf = create_grid(-4, 4, -4, 4, 0.5)

    # Ejemplo de uso de la función
    save_grid_as_texture(grid_gdf)

    #############################################################
    #### Desde aqui se genera la escena ####

    # Crear un plotter
    plotter = pv.Plotter()

    # Iterar sobre cada fila en el GeoDataFrame
    for idx, row in gdf.iterrows():

        polygon = row['geometry']
        height = row['Height']

        if(height > 0):
            # Crear la malla principal y las mallas de las caras laterales
            main_mesh, side_meshes = create_prism_mesh_and_sides(polygon, height)

            # Añadir la malla principal al plotter
            plotter.add_mesh(main_mesh)  # Sin textura o con una textura específica

            # Añadir cada malla de cara lateral con su textura
            for side_mesh in side_meshes:
                plotter.add_mesh(side_mesh)

            roof_mesh = create_roof_shape(
                polygon,
                base_height=height,
                expansion_factor=1.20,
                roof_height_factor=0.5)
            
            plotter.add_mesh(roof_mesh)

        else:
            mesh = create_flat_mesh(polygon)
            plotter.add_mesh(mesh)  # Sin textura o con una textura específica

    # Exportar la escena actual como un archivo .obj
    plotter.export_obj("tu_escena.stl")

    # Cerrar el plotter
    plotter.close()

    # Cargar el objeto 3D
    mesh_3d = pv.read('tu_escena.obj')

    # Cargar la textura
    texture = pv.read_texture('heatmap.png')

    # Aplicar la textura al objeto 3D
    # Esto asume que tu objeto 3D tiene coordenadas de textura adecuadas
    mesh_3d.texture_map_to_plane(inplace=True)  # Puede que necesites ajustar esto
    plotter = pv.Plotter()
    plotter.add_mesh(mesh_3d, texture=texture)
    plotter.show()

if __name__=='__main__':
    main()
