import geopandas as gpd
from shapely.geometry import Point, LineString, MultiLineString, Polygon, MultiPolygon
import pyvista as pv
import warnings
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import pandas as pd
import joblib
from myfunctions import *
import os

# Desactiva todos los warnings
warnings.filterwarnings("ignore")


# if os.path.exists(filename):
#     pass
# else:
#     pass

edificaciones_gdf = gpd.read_file('./data/construcciones_maqueta')
edificaciones_gdf.rename(columns={'Metros': 'Height'}, inplace=True)
edificaciones_gdf.dropna(subset=['geometry'], inplace=True)
curvas_nivel_gdf = gpd.read_file('data/Maqueta')
curvas_nivel_gdf.rename(columns={'CONTOUR': 'elevation'}, inplace=True)
unit = gpd.read_file('./data/grid')
desired_crs = 'EPSG:32718'

print('1.- Carga de datos')
edificaciones_gdf = check_and_assign_crs(edificaciones_gdf, desired_crs)
curvas_nivel_gdf = check_and_assign_crs(curvas_nivel_gdf, desired_crs)
unit = check_and_assign_crs(unit, desired_crs)

x_min, x_max, y_min, y_max = obtener_limites_geodf(curvas_nivel_gdf)
esquinas_gdf = limites_a_puntos_geodf(x_min, x_max, y_min, y_max)

print('2.- Interpolando curva')
filename = './data/intermediate/interpolation.parquet'
if os.path.exists(filename):
    mesh_gdf = gpd.read_parquet(filename)
    pass
else:
    mesh_df = interpolate_curves(curvas_nivel_gdf)

    # Aplicar la función para convertir mesh_df a un GeoDataFrame
    mesh_gdf = convert_mesh_to_gdf(mesh_df)
    mesh_gdf = mesh_gdf.set_crs(desired_crs)
    mesh_gdf.to_parquet(filename)
    pass

print('3.- Calculando niveles de edificaciones')
filename = './data/intermediate/update_buildings.parquet'
if os.path.exists(filename):
    updated_buildings_gdf = gpd.read_parquet(filename)
    pass
else:
    updated_buildings_gdf = calculate_terrain_stats_for_buildings(edificaciones_gdf, mesh_gdf)
    updated_buildings_gdf.to_parquet(filename)
    pass

print('4.- Estimacion de altura')
filename = './data/intermediate/data_pred.parquet'
if os.path.exists(filename):
    data = gpd.read_parquet(filename)
    pass
else:
    knn_model = joblib.load('./knn_model.pkl')
    centroids_in = updated_buildings_gdf.loc[updated_buildings_gdf['max_terrain_height'].isna(), 'geometry'].centroid
    data = {
        'x': centroids_in.x.values,
        'y': centroids_in.y.values,
    }
    data = pd.DataFrame.from_dict(data)
    data['max_terrain_height_pred'] = knn_model.predict(data)
    data = convert_mesh_to_gdf(data)
    data.to_parquet(filename)
    pass

updated_buildings_gdf['x'] = updated_buildings_gdf['geometry'].centroid.x
updated_buildings_gdf['y'] = updated_buildings_gdf['geometry'].centroid.y

print('5.- Ajuste de alturas')
filename = './data/intermediate/merge_heights.parquet'
if os.path.exists(filename):
    merge_gdf = gpd.read_parquet(filename)
    pass
else:
    merge_gdf = pd.merge(updated_buildings_gdf, data.drop(columns=['geometry']), how='outer', on=['x','y'])
    [merge_gdf[col].fillna(0, inplace=True) for col in ['max_terrain_height', 'max_terrain_height_pred']];
    merge_gdf['baseline_height'] = merge_gdf[['max_terrain_height', 'max_terrain_height_pred']].sum(axis=1)
    merge_gdf.rename(columns={'Height': 'building_height'}, inplace=True)
    merge_cols = ['building_height', 'baseline_height', 'geometry']
    merge_gdf = merge_gdf[merge_cols]
    merge_gdf['z'] = merge_gdf[['building_height', 'baseline_height']].sum(axis=1)
    merge_gdf.to_parquet(filename)
    pass


print('6.- Calculo de máxima altura por grid')
filename = './data/intermediate/Legotization.parquet'
if os.path.exists(filename):
    grid_gdf = gpd.read_parquet(filename)
    pass
else:
    grid_with_max_heights = calculate_max_height_for_grid(unit, merge_gdf, mesh_gdf)

    values = grid_with_max_heights['max_height']

    vmin, vmax = 0, 36
    grid_with_max_heights['LEGO'] = map_values_to_range(values, vmin, vmax)

    grid_gdf = grid_with_max_heights.copy()
    grid_gdf.to_parquet('Legotization.parquet')
    pass


meshes = []
[meshes.append(create_prism_mesh_and_sides(row['geometry'], row['max_height'])) for index, row in grid_gdf.iterrows()];

plotter = pv.Plotter()

for resultados in meshes:
    for resultado in resultados:
        plotter.add_mesh(resultado[0])
        for sample in resultado[1]:
            plotter.add_mesh(sample)

# Exporta la escena a un archivo OBJ
output_file = 'Legotizacion.obj'
plotter.export_obj(output_file)
plotter.show()
