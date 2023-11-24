import geopandas as gpd
from shapely.geometry import Point, LineString, MultiLineString, Polygon, MultiPolygon
import pyvista as pv
import warnings
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import pandas as pd

# Desactiva todos los warnings
warnings.filterwarnings("ignore")

# Función para verificar y asignar CRS
def check_and_assign_crs(gdf, desired_crs):
    if gdf.crs is None or gdf.crs != desired_crs:
        gdf = gdf.to_crs(desired_crs)
    return gdf

def obtener_limites_geodf(geodf):
    """
    Calcula los límites espaciales (x_min, x_max, y_min, y_max) de un GeoDataFrame.

    :param geodf: GeoDataFrame con geometrías LineString.
    :return: Tupla con los valores (x_min, x_max, y_min, y_max).
    """
    x_min, x_max, y_min, y_max = float('inf'), float('-inf'), float('inf'), float('-inf')

    for linea in geodf.geometry:
        bounds = linea.bounds
        x_min, y_min = min(x_min, bounds[0]), min(y_min, bounds[1])
        x_max, y_max = max(x_max, bounds[2]), max(y_max, bounds[3])

    return x_min, x_max, y_min, y_max

def limites_a_puntos_geodf(x_min, x_max, y_min, y_max):
    """
    Convierte los límites en un GeoDataFrame con los cuatro puntos de esquina.

    :param x_min: Límite mínimo en el eje X.
    :param x_max: Límite máximo en el eje X.
    :param y_min: Límite mínimo en el eje Y.
    :param y_max: Límite máximo en el eje Y.
    :return: GeoDataFrame con los cuatro puntos de esquina.
    """
    # Crear los puntos de esquina
    puntos = [
        Point(x_min, y_min),
        Point(x_min, y_max),
        Point(x_max, y_min),
        Point(x_max, y_max)
    ]

    # Crear un GeoDataFrame
    gdf = gpd.GeoDataFrame(geometry=puntos)

    return gdf

def interpolate_curves(curvas_nivel_gdf):
    # Extraer los puntos y las elevaciones de las curvas de nivel
    points = []
    elevations = []
    
    for index, row in curvas_nivel_gdf.iterrows():
        geom = row['geometry']

        # Verificar si la geometría es un LineString
        if isinstance(geom, LineString):
            for coord in list(geom.coords):
                points.append(coord[:2])  # Coordenadas x, y
                elevations.append(row['elevation'])  # Elevación

        # Verificar si la geometría es un MultiLineString
        elif isinstance(geom, MultiLineString):
            for linestring in geom.geoms:
                for coord in list(linestring.coords):
                    points.append(coord[:2])
                    elevations.append(row['elevation'])

    # Convertir a array de numpy
    points_array = np.array(points)
    elevations_array = np.array(elevations)

    # Crear una cuadrícula para la interpolación
    x_min, x_max, y_min, y_max = obtener_limites_geodf(curvas_nivel_gdf)
    grid_x, grid_y = np.mgrid[x_min:x_max:1000j, y_min:y_max:1000j]

    # Interpolación de los datos
    grid_z = griddata(points_array, elevations_array, (grid_x, grid_y), method='linear')

    # Extraer las coordenadas x, y, z del mesh
    x_coords = grid_x.flatten()
    y_coords = grid_y.flatten()
    z_coords = grid_z.flatten()

    # Eliminar valores NaN resultantes de la interpolación
    valid_indices = ~np.isnan(z_coords)
    x_valid = x_coords[valid_indices]
    y_valid = y_coords[valid_indices]
    z_valid = z_coords[valid_indices]

    # Crear un nuevo DataFrame con x, y, z
    mesh_df = pd.DataFrame({'x': x_valid, 'y': y_valid, 'z': z_valid})

    return mesh_df

def convert_mesh_to_gdf(mesh_df):
    """
    Convierte un DataFrame con columnas x, y, z en un GeoDataFrame con geometrías tipo Point.

    Args:
    mesh_df (pd.DataFrame): DataFrame con columnas 'x', 'y', 'z'.

    Returns:
    gpd.GeoDataFrame: GeoDataFrame con la geometría de puntos y los datos de elevación.
    """

    # Crear geometrías de punto a partir de las coordenadas x, y
    geometry = [Point(xy) for xy in zip(mesh_df.x, mesh_df.y)]

    # Crear un GeoDataFrame
    mesh_gdf = gpd.GeoDataFrame(mesh_df, geometry=geometry)

    return mesh_gdf


def calculate_terrain_stats_for_buildings(buildings_gdf, terrain_gdf):
    """
    Calcula los valores máximo, mínimo y promedio de las alturas del terreno para cada edificación.

    Args:
    buildings_gdf (gpd.GeoDataFrame): GeoDataFrame de las edificaciones.
    terrain_gdf (gpd.GeoDataFrame): GeoDataFrame con las alturas del terreno.

    Returns:
    gpd.GeoDataFrame: GeoDataFrame de las edificaciones con los valores estadísticos agregados.
    """
    # Asegurarse de que los GeoDataFrames estén en el mismo sistema de coordenadas
    if buildings_gdf.crs != terrain_gdf.crs:
        terrain_gdf = terrain_gdf.to_crs(buildings_gdf.crs)

    # Inicializar listas para almacenar los valores estadísticos
    max_heights, min_heights, mean_heights = [], [], []

    # Iterar sobre cada edificación
    for _, building in buildings_gdf.iterrows():
        # Encontrar los puntos del terreno que están dentro de la edificación
        within_building = terrain_gdf[terrain_gdf.within(building.geometry)]

        # Calcular estadísticas si hay puntos dentro de la edificación
        if not within_building.empty:
            max_heights.append(within_building['z'].max())
            min_heights.append(within_building['z'].min())
            mean_heights.append(within_building['z'].mean())
        else:
            max_heights.append(np.nan)
            min_heights.append(np.nan)
            mean_heights.append(np.nan)

    # Agregar las estadísticas al GeoDataFrame de las edificaciones
    buildings_gdf['max_terrain_height'] = max_heights
    buildings_gdf['min_terrain_height'] = min_heights
    buildings_gdf['mean_terrain_height'] = mean_heights

    return buildings_gdf

def calculate_max_height_for_grid(grid_gdf, merge_gdf, mesh_gdf):
    """
    Calcula la altura máxima en cada cuadrícula del grid, utilizando dos GeoDataFrames:
    uno con la altura de edificaciones sobre el terreno y otro con la altura del terreno.

    Args:
    grid_gdf (gpd.GeoDataFrame): GeoDataFrame con las cuadrículas.
    merge_gdf (gpd.GeoDataFrame): GeoDataFrame con alturas de edificaciones sobre el terreno.
    mesh_gdf (gpd.GeoDataFrame): GeoDataFrame con alturas del terreno.

    Returns:
    gpd.GeoDataFrame: GeoDataFrame de las cuadrículas con la altura máxima en cada una.
    """
    max_heights = []

    # Asegurarse de que todos los GeoDataFrames estén en el mismo sistema de coordenadas
    if grid_gdf.crs != merge_gdf.crs:
        merge_gdf = merge_gdf.to_crs(grid_gdf.crs)

    if grid_gdf.crs != mesh_gdf.crs:
        mesh_gdf = mesh_gdf.to_crs(grid_gdf.crs)

    # Iterar sobre cada cuadrícula en el grid
    for _, grid_cell in grid_gdf.iterrows():
        # Encontrar las edificaciones que intersectan con la cuadrícula
        intersecting_buildings = merge_gdf[merge_gdf.intersects(grid_cell.geometry)]

        # Encontrar los puntos del terreno que están dentro de la cuadrícula
        intersecting_terrain = mesh_gdf[mesh_gdf.within(grid_cell.geometry)]

        # Determinar la altura máxima
        if not intersecting_buildings.empty:
            # Usar la altura de las edificaciones si hay alguna en la cuadrícula
            max_height = intersecting_buildings['z'].max()
        elif not intersecting_terrain.empty:
            # Usar la altura del terreno si no hay edificaciones
            max_height = intersecting_terrain['z'].max()
        else:
            # Si no hay ni edificaciones ni terreno, asignar NaN
            max_height = np.nan

        max_heights.append(max_height)

    # Agregar la columna de alturas máximas al GeoDataFrame del grid
    grid_gdf['max_height'] = max_heights

    return grid_gdf

def map_values_to_range(values, vmin, vmax):
    """
    Mapea una lista de valores a un rango de valores enteros entre vmin y vmax.

    Args:
    values (list): Lista de valores a mapear.
    vmin (int): Valor mínimo del rango objetivo.
    vmax (int): Valor máximo del rango objetivo.

    Returns:
    list: Lista de valores mapeados al rango especificado.
    """
    # Convertir la lista a un array de numpy para facilitar el cálculo
    values_array = np.array(values)

    # Normalizar los valores para que estén entre 0 y 1
    normalized = (values_array - np.min(values_array)) / (np.max(values_array) - np.min(values_array))

    # Escalar los valores normalizados al rango deseado y convertirlos a enteros
    scaled_values = (normalized * (vmax - vmin) + vmin).astype(int)

    return scaled_values.tolist()


def create_prism_mesh_and_sides(input_polygon, height, h0=0):
    # Verificar si es un MultiPolygon y convertirlo a una lista de polígonos si es necesario
    if isinstance(input_polygon, MultiPolygon):
        polygons = list(input_polygon.geoms)
    elif isinstance(input_polygon, Polygon):
        polygons = [input_polygon]
    else:
        raise ValueError("Input debe ser un Polygon o MultiPolygon")

    # Inicializar una lista para almacenar los resultados de cada polígono
    result_meshes = []

    # Iterar sobre los polígonos
    for polygon in polygons:
        # Extraer los puntos x, y del polígono
        x, y = polygon.exterior.coords.xy

        # Crear los puntos para las caras superiores e inferiores
        top_points = [(xi, yi, height + h0) for xi, yi in zip(x, y)]
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

        # Agregar el resultado de este polígono a la lista de resultados
        result_meshes.append((main_mesh, side_meshes))

    return result_meshes