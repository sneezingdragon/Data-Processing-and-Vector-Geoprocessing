import pandas as pd
import geopandas as gpd
import fiona
treasure = gpd.read_file('C:/Users/sneez/Downloads/lab1/lab1.gpkg')
layers = fiona.listlayers('C:/Users/sneez/Downloads/lab1/lab1.gpkg')
print(layers)
polygons = []
tables = []

for layer_name in layers:
        if layer_name.startswith('soilmu'):
            polygons.append(layer_name)
            
for layer_name in layers:
    if layer_name.startswith('muaggatt'):
        tables.append(layer_name)
for idx, poly in enumerate(polygons):
    print(poly, tables[idx], idx)
for spatial in polygons:
    layer_id = spatial[-5:]
    for table in tables:
        if table[-5:] == layer_id:
            print(spatial, table)
result = []
joined_list = []
for poly in polygons:
    for table in tables:
        if poly [-5:] == table [-5:]:
            p = gpd.read_file('C:/Users/sneez/Downloads/lab1/lab1.gpkg', layer= poly)
            t = gpd.read_file('C:/Users/sneez/Downloads/lab1/lab1.gpkg', layer= table)
            t = t.drop(columns = 'geometry')
            result = pd.merge(p, t, left_on= 'MUSYM', right_on='musym')
            result['mapunit'] = (poly[-5:])
            joined_list.append(result)
merged = pd.concat(joined_list)
merged.head()
watershed = gpd.read_file('C:/Users/sneez/Downloads/lab1/lab1.gpkg', layer='wbdhu8_lab1')
watershed
intersect = gpd.overlay(merged, watershed, how='intersection')
summary = intersect.groupby(by='NAME').count()
for idx, row in summary.iterrows():
    features = row['SPATIALVER']
    print(f'{features} classes in watershed {idx}')