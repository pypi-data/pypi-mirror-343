def one():
    print('''

pip install osmnx
pip install folium
pip install keplergl
pip install osmnx==1.3.0

import osmnx as ox
print(ox.__version__)
#
import osmnx as o
import networkx as nx
import matplotlib.pyplot as plt
import folium
import random
from keplergl import KeplerGl
place_name = "Mumbai, Maharashtra, India"
graph = ox.graph_from_place(place_name)
ox.plot_graph(graph)
#
ox.plot_graph_folium(graph)
#
area = ox.geocode_to_gdf(place_name)
area.head()
#
area.plot()
#
buildings = ox.geometries_from_place(place_name, tags={"building":
True})
buildings.plot()
#
restaurants = ox.geometries_from_place(place_name, tags={"amenity":
"restaurant"})
restaurants.plot()
#
nodes, edges = ox.graph_to_gdfs(graph)
nodes.plot()
#
edges.plot()
fig, ax = plt.subplots(figsize=(10, 14))
area.plot(ax=ax, facecolor='white')
edges.plot(ax=ax, linewidth=1, edgecolor='blue')
buildings.plot(ax=ax, facecolor='yellow', alpha=0.7)
restaurants.plot(ax=ax, color='red', alpha=0.9, markersize=12)
plt.tight_layout()
#
K_map = KeplerGl()
buildings = ox.geometries_from_place(place_name, tags={"building":
True})
restaurants = ox.geometries_from_place(place_name, tags={"amenity":
"restaurant"})
K_map.add_data(data=restaurants, name='Restaurants')
K_map.add_data(data=buildings, name='Buildings')
K_map.save_to_html()
#
ox.plot_route_folium(graph, route, route_linewidth=6, node_size=0)
#
restaurant_1, restaurant_2 =
random.sample(restaurants.index
.tolist(), 2)
rest_1_coords =
(restaurants.loc[restaurant_1].
geometry.y,
restaurants.loc[restaurant_1].g
eometry.x)
rest_2_coords =
(restaurants.loc[restaurant_2].
geometry.y,
restaurants.loc[restaurant_2].g
eometry.x)
start_node =
ox.distance.nearest_nodes(graph
, rest_1_coords[1],
rest_1_coords[0])
end_node =
ox.distance.nearest_nodes(graph
, rest_2_coords[1],
rest_2_coords[0])
route = nx.shortest_path(graph,
start_node, end_node,
weight='length')
fig, ax =
ox.plot_graph_route(graph,
route, route_linewidth=6,
node_size=0, bgcolor='w',
figsize=(10, 14))
ox.plot_route_folium(graph,
route, route_linewidth=6,
node_size=0)
plt.show()
ox.plot_route_folium(graph, route, route_linewidth=6, node_size=0)

''')
    
def two():
    print('''

pip install geopandas
pip install pyogrio

Setting Coordinate Systems with GeoPandas
import os
import geopandas as gpd
gdf = gpd.read_file('/content/IND_adm0.shp')
print("Calculating CRS for IND_adm0.shp file: ")
print("Current CRS for IND_adm0.shp file:", gdf.crs
gdf = gdf.set_crs(epsg=4326)
print("After updating CRS of shapefile\nUpdated CRS for IND_adm0.shp
file:", gdf.crs)
#
Converting Coordinate Systems with Pyproj
from pyproj import Transformer
source_crs = 'epsg:4326'
target_crs = 'epsg:3857'
transformer = Transformer.from_crs(source_crs, target_crs)

longitude, latitude = 72.8777, 19.0760
x, y = transformer.transform(latitude, longitude)
print(f"Original coordinates: ({longitude}, {latitude})")
print(f"Transformed coordinates: ({x}, {y})")
#
Reprojecting a GeoDataFrame with GeoPandas
import geopandas as gpd
print("Current CRS:", gdf.crs)
gdf_reprojected = gdf.to_crs(epsg=32643)
print("Reprojected CRS:", gdf_reprojected.crs)
gdf_reprojected.to_file('path_to_reprojected_shapefile.shp')
#
Converting Coordinates Using Shapely and Pyproj
from shapely.geometry import Point
from pyproj import Transformer
source_crs = 'epsg:4326'
target_crs = 'epsg:32643'
transformer = Transformer.from_crs(source_crs, target_crs)
coordinates = [(72.8777, 19.0760), (77.1025, 28.7041)]
transformed_coordinates = [transformer.transform(lat, lon) for lon,
lat in coordinates]
print("Original coordinates:", coordinates)
print("Transformed coordinates:", transformed_coordinates)

''')
    
def three():
    print('''

pip install pandas
pip install numpy
pip install scipy

import pandas as pd
import numpy as np
from scipy import stats
rainfall =
pd.read_csv("Rainfall_In_India_2005_09_missingvalues(in).csv")
print("Initial Dataset:\n", rainfall.head())
#
print("Missing Values Before Handling:\n", rainfall.isnull().sum())
#
num_cols = rainfall.select_dtypes(include=[np.number]).columns
rainfall[num_cols] = rainfall[num_cols].apply(lambda x:
x.fillna(x.median()))
cat_cols = rainfall.select_dtypes(include =['object']).columns
for cols in cat_cols:
rainfall[cols] = rainfall[cols].fillna(rainfall[cols].mode()[0])
print("\n Missing Value After Handling:\n",rainfall.isnull().sum())
#
def
remove_outliers(rainfall,col,thresold = 3):
z_scores = np.abs (stats.zscore(rainfall[col]))
return rainfall[z_scores < thresold]
for col in num_cols:
rainfall = remove_outliers(rainfall, col)
print("After Handling Outliers:", rainfall.shape)
#
rainfall = rainfall.drop_duplicates()
rainfall.columns =[col.strip().lower().replace(" "," ") for col in
rainfall.columns]
cat_cols = rainfall.select_dtypes(include = ['object']).columns
num_cols = rainfall.select_dtypes(include = [np.number]).columns
rainfall[cat_cols] = rainfall[cat_cols].astype(str)
rainfall[num_cols] = rainfall[num_cols].apply(pd.to_numeric, errors
= 'coerce')
print("Final Cleaned Dataset:\n",rainfall.head())
#
cleaned_file_path = "Cleaned_Rainfall_Data.csv"
rainfall.to_csv(cleaned_file_path, index = False)
print(f"Cleaned dataset saved as:{cleaned_file_path}")

''')
    
def four():
    print('''

pip install geoplot

import geopandas as gpd
import geoplot.crs as gcrs
import geoplot as gplt
import matplotlib.pyplot as plt
geoData = gpd.read_file(
'https://raw.githubusercontent.
com/holtzy/The-Python-GraphGallery/master/static/data/UScounties.geojson'
)
geoData.id =
geoData['id'].astype(int)
statesToRemove = ['02', '15',
'72']
geoData =
geoData[~geoData.STATE.isin(sta
tesToRemove)]
gplt.polyplot(
geoData,
projection=gcrs.AlbersEqualArea
()
)
plt.show()
#
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
data = pd.read_csv(
'https://raw.githubusercontent.com/holtzy/The-Python-Graph Gallery/master/static/data/unemployment-x.csv')
sns.histplot(data["rate"])
plt.show()
#
fullData = geoData.merge(
data,
left_on=['id'],
right_on=['id']
)fullData.head(3)
#
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import mapclassify as mc
scheme = mc.Quantiles(fullData['rate'], k=10)
gplt.choropleth(
fullData,
projection=gcrs.AlbersEqualArea(),
hue="rate",
scheme=scheme, cmap='inferno_r',
linewidth=.1,
edgecolor='black',
figsize=(12, 8))
#
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
df =
pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/mast
er/fips-unemp-16.csv",
dtype={"fips": str})
import seaborn as sns
sns.set_theme(style="darkgrid")
sns.histplot(data=df, x="unemp")
plt.show();
#
from urllib.request import
urlopen
import json
with
urlopen('https://raw.githubuser
content.com/plotly/datasets/mas
t e r / g e o j s o n - c o u n t i e s -
fips.json') as response:
counties =
json.load(response)
import plotly.express as px
fig = px.choropleth(df,
geojson=counties,
locations='fips',
color='unemp',
color_continuous_scale="Viridis
",
range_color=(0, 12),
labels={'unemp':'unemployment
rate'}
)
fig.update_layout(margin={"r":0
,"t":0,"l":0,"b":0})
fig.update_layout(coloraxis_col
orbar=dict(
thicknessmode="pixels",
thickness=10,
lenmode="pixels", len=150,
yanchor="top", y=0.8,
ticks="outside",
ticksuffix=" %",
dtick=5
))
fig.show()
''')

def help():
    print('''
one() = 1c: Collecting geospatial data from various sources and visualizing data
two() = 2a: Convert spatial data between different Coordinate Reference Systems
three() = 3a: Handling Missing Data and Outliers
four() = 9: Create Thematic Maps for Visualize
''')