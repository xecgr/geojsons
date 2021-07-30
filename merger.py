from shapely.geometry import shape,mapping
from shapely.ops import unary_union
import csv
import glob
import json



cod__name = {}
with open('municipios.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cod__name[row['municipio_id']]=row


ext  = "geojson"
path = "inputs"
expr = "{}/*.{}".format(path,ext)
municipio__polygons = {}
for file_path in glob.glob(expr):
    items = json.load( open( file_path, "r" ) )
    features = items["features"]
    for f in features: 
        municipio = str(f['properties']['CODIGO_INE']).zfill(5)
        municipio__polygons.setdefault(
            municipio,[]
        ).append(
            shape(f['geometry'])
        )


merged_features = []
for municipio,polygons in municipio__polygons.items():
    p1       = unary_union(polygons)
    _feature = {
        "type":"Feature",
        "properties":cod__name.get(municipio,''),
        "geometry":mapping(p1)
    }
    merged_features.append(_feature)

geojson = {
    "type":"FeatureCollection",
    "features":merged_features
}

file_path = 'output/catalunya.geojson'
json.dump(geojson, open(file_path, "w" ))

