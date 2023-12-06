import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon, Point, Polygon, MultiPolygon
import matplotlib.colors as mcolors
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image
from sklearn.decomposition import PCA
from shapely.affinity import rotate

import warnings

# Desactivar todos los warnings
warnings.filterwarnings('ignore')


def plot_grid(gdf, font_size):
    # Configurar el tamaño de la figura para A4
    fig, ax = plt.subplots(1, 1, figsize=(11.7, 8.3))  # Tamaño A4 en pulgadas

    # Graficar el GeoDataFrame
    gdf.plot(ax=ax, color='white', edgecolor='black', alpha=0.9)

    # Añadir anotaciones de 'legos'
    for idx, row in gdf.iterrows():
        plt.text(row['geometry'].centroid.x, row['geometry'].centroid.y, str(row['legos']), 
                 ha='center', va='center', fontsize=font_size,
                 color=mcolors.to_hex(plt.cm.RdYlGn(row['legos']/30)))

    # Guardar la figura
    output_dir = "/data/output"
    os.makedirs(output_dir, exist_ok=True)
    image_path = f"{output_dir}/mapa01.png"
    plt.axis(False)
    plt.savefig(image_path, bbox_inches='tight')
    return image_path

def image_to_pdf(image_path):
    # Tamaño de A4 en puntos
    a4_width_pt, a4_height_pt = A4
    # Cargar imagen para obtener sus dimensiones
    with Image.open(image_path) as img:
        img_width, img_height = img.size

    # Calcular el escalado manteniendo la relación de aspecto
    ratio = min(a4_width_pt / img_width, a4_height_pt / img_height)
    new_width = img_width * ratio
    new_height = img_height * ratio

    # Calcular las coordenadas para centrar la imagen
    x_center = (a4_width_pt - new_width) / 2
    y_center = (a4_height_pt - new_height) / 2

    # Crear PDF y añadir la imagen centrada
    c = canvas.Canvas(image_path.replace('.png', '.pdf'), pagesize=A4)
    c.drawImage(image_path, x_center, y_center, width=new_width, height=new_height)
    c.showPage()
    c.save()

def calculate_rotation_angle(gdf):
    # Extraer los centroides de los polígonos y multipolígonos
    centroids = gdf.geometry.centroid
    points = np.array([[p.x, p.y] for p in centroids])

    # Aplicar PCA para encontrar la orientación principal
    pca = PCA(n_components=2)
    pca.fit(points)
    principal_axis = pca.components_[0]

    # Calcular el ángulo de rotación
    angle = np.arctan2(principal_axis[1], principal_axis[0])
    angle_degrees = np.degrees(angle)

    return angle_degrees

def rotate_point(x, y, angle_rad):
    """Rotar un punto alrededor del origen (0, 0)"""
    x_rot = x * np.cos(angle_rad) - y * np.sin(angle_rad)
    y_rot = x * np.sin(angle_rad) + y * np.cos(angle_rad)
    return x_rot, y_rot

def plot_rotated_gdf(gdf, angle_degrees, output_dir):
    angle_rad = np.radians(angle_degrees)

    fig, ax = plt.subplots(1, 1, figsize=(11.7, 8.3))  # Tamaño A4 en pulgadas

    for idx, row in gdf.iterrows():
        x, y = row['geometry'].centroid.x, row['geometry'].centroid.y
        x_rot, y_rot = rotate_point(x, y, angle_rad)
        plt.plot(x_rot, y_rot, 'o')  # Plotear el punto rotado
    image_path = f"{output_dir}/mapa02.png"
    # plt.ylim([-1, 1])
    plt.savefig(image_path, bbox_inches='tight')
    return image_path

def plot_rotated_poly_gdf(gdf, angle_degrees, output_dir):
    angle_rad = np.radians(angle_degrees)
    fig, ax = plt.subplots(1, 1, figsize=(11.7, 8.3))  # Tamaño A4 en pulgadas

    # Rotar cada geometría en el GeoDataFrame
    rotated_gdf = gdf.copy()
    rotated_gdf['geometry'] = gdf['geometry'].apply(lambda geom: rotate(geom, angle_rad, origin="center"))

    rotated_gdf.plot(ax=ax)
    gdf.plot(ax=ax, color='red', alpha=0.3, edgecolor='black', linewidth=2)

    image_path = f"{output_dir}/mapa03.png"
    # Rotar cada geometría en el GeoDataFrame
    for geom in gdf.geometry:
        rotated_geom = rotate(geom, angle_degrees, origin='centroid')
        gpd.GeoSeries([rotated_geom]).plot(ax=ax)
    plt.savefig(image_path, bbox_inches='tight')
    return image_path

def generate_data():
    # Generar puntos que formen una línea inclinada
    angle_degrees = 100  # Puedes cambiar este ángulo para probar diferentes inclinaciones
    angle_radians = np.radians(angle_degrees)
    num_points = 20
    x_start, y_start = 0, 0
    x_end, y_end = 10, 10 * np.tan(angle_radians)

    x_coords = np.linspace(x_start, x_end, num_points)
    y_coords = np.linspace(y_start, y_end, num_points)

    points = [Point(x, y) for x, y in zip(x_coords, y_coords)]

    # Crear un GeoDataFrame
    gdf = gpd.GeoDataFrame(geometry=points)
    return gdf

def create_rotated_polygon(x_center, y_center, angle_degrees, width, height):
    angle_radians = np.radians(angle_degrees)
    cos_angle = np.cos(angle_radians)
    sin_angle = np.sin(angle_radians)

    # Coordenadas del rectángulo antes de la rotación
    corners = [
        (x_center - width / 2, y_center - height / 2),
        (x_center + width / 2, y_center - height / 2),
        (x_center + width / 2, y_center + height / 2),
        (x_center - width / 2, y_center + height / 2)
    ]

    # Rotar cada esquina
    rotated_corners = [
        (x * cos_angle - y * sin_angle, x * sin_angle + y * cos_angle)
        for x, y in corners
    ]

    return Polygon(rotated_corners)

def generate_poly_data(num_samples=10):
    # Crear polígonos y multipolígonos
    num_samples = num_samples
    polygons = []
    for i in range(num_samples):
        angle = np.random.uniform(0, 30)  # Ángulo aleatorio entre 45 y 70 grados
        if i % 2 == 0:  # Polígonos simples
            polygon = create_rotated_polygon(i * 10, 0, angle, 5, 8)
            polygons.append(polygon)
        else:  # Multipolígonos
            polygon1 = create_rotated_polygon(i * 10, 0, angle, 5, 8)
            polygon2 = create_rotated_polygon(i * 10 + 5, 5, angle, 3, 4)
            multipolygon = MultiPolygon([polygon1, polygon2])
            polygons.append(multipolygon)

    # Crear un GeoDataFrame
    gdf = gpd.GeoDataFrame(geometry=polygons)
    return gdf

def plot_with_rotated_view(gdf, angle_degrees):
    fig, ax = plt.subplots(figsize=(11.7, 8.3))  # Tamaño A4 en pulgadas

    # Calcular la transformación de los ejes
    angle_radians = np.radians(angle_degrees)
    cos_angle = np.cos(angle_radians)
    sin_angle = np.sin(angle_radians)
    ax.set_aspect(cos_angle / sin_angle)

    gdf.plot(ax=ax)

    # Ajustar los límites del eje si es necesario
    xmin, ymin, xmax, ymax = gdf.total_bounds
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])
    plt.savefig('/data/output/mapa05.png', bbox_inches='tight')

# gdf = generate_poly_data()

# image_path = '/data/output'
# # Suponiendo que gdf es tu GeoDataFrame
# angle = calculate_rotation_angle(gdf)
# print(angle)
# plot_rotated_poly_gdf(gdf, -angle, image_path)  # Rotar en sentido contrario al ángulo calculado


# gdf['legos'] = np.nan
# # Llamar a la función plot_grid y luego a image_to_pdf
# image_path = plot_grid(gdf, font_size=20)
# image_to_pdf(image_path)

import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon, MultiPolygon, LineString, MultiLineString
from shapely.ops import unary_union
import pandas as pd

def rotate_point(point, angle, origin):
    """Rotar un punto alrededor de un origen dado."""
    ox, oy = origin
    px, py = point

    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)

    return qx, qy

def rotate_geometry(geom, angle, origin):
    """Rotar una geometría (polígono, línea) alrededor de un origen dado."""
    if geom.type == 'Polygon':
        exterior = [rotate_point(p, angle, origin) for p in geom.exterior.coords]
        interiors = [[rotate_point(p, angle, origin) for p in interior.coords] for interior in geom.interiors]
        return Polygon(exterior, interiors)
    elif geom.type == 'MultiPolygon':
        polygons = [rotate_geometry(part, angle, origin) for part in geom.geoms]
        return MultiPolygon(polygons)
    elif geom.type == 'LineString':
        return LineString([rotate_point(p, angle, origin) for p in geom.coords])
    elif geom.type == 'MultiLineString':
        return MultiLineString([rotate_geometry(part, angle, origin) for part in geom])
    else:
        # Añadir manejo para otros tipos de geometrías si es necesario
        return geom

def rotate_gdf(gdf, angle_degrees):
    """Rotar todas las geometrías en un GeoDataFrame."""
    angle_radians = np.radians(angle_degrees)

    # Encontrar el centro de todos los datos
    all_points = [geom.centroid for geom in gdf.geometry]
    all_points = gpd.GeoDataFrame(geometry=all_points)
    all_points['x'] = all_points.geometry.x
    all_points['y'] = all_points.geometry.y
    print()
    
    center = all_points[['x','y']].mean()
    # center = (0, 100)

    # Rotar cada geometría
    rotated_geoms = gdf.geometry.apply(lambda geom: rotate_geometry(geom, angle_radians, center))

    return gpd.GeoDataFrame(gdf[['geometry']], geometry=rotated_geoms)

gdf = generate_poly_data()

image_path = '/data/output'
# Suponiendo que gdf es tu GeoDataFrame con polígonos, líneas, etc.
angle = -60  # Ángulo de rotación en grados
rotated_gdf = rotate_gdf(gdf, angle)

# Ahora puedes plotear rotated_gdf como lo harías normalmente
import matplotlib.pyplot as plt
import os

def plot_and_save_gdf(gdf, file_path):
    fig, ax = plt.subplots(figsize=(10, 10))  # Puedes ajustar el tamaño según tus necesidades
    gdf.plot(ax=ax)

    # Ajustar los límites del eje si es necesario
    xmin, ymin, xmax, ymax = gdf.total_bounds
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

    # Guardar el gráfico como un archivo .png
    plt.savefig(file_path, dpi=300)  # Ajusta el dpi según tus necesidades
    plt.close(fig)

# Suponiendo que rotated_gdf es tu GeoDataFrame rotado
output_folder = "/data/output"
output_file = "mapa06.png"
output_path = os.path.join(output_folder, output_file)

# Crear la carpeta si no existe
os.makedirs(output_folder, exist_ok=True)

# Plotear y guardar el GeoDataFrame
plot_and_save_gdf(rotated_gdf, output_path)
plot_and_save_gdf(gdf, output_path.replace('06','07'))
