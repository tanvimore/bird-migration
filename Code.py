import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import  Point, LineString

#Dataframe
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
america = world.loc[world['continent'].isin(['North America','South America'])]
south_america = america.loc[america['continent'] == 'South America']
birds_df = pd.read_csv("C:/Users/TanviMore/Desktop/DataAnalytics/purple_martin.csv", parse_dates=['timestamp'])
print("*********ANALYSIS*********")
print("There are {} different birds in the dataset.".format(birds_df["tag-local-identifier"].nunique()))
birds = gpd.GeoDataFrame(birds_df, geometry= gpd.points_from_xy(birds_df["location-long"], birds_df["location-lat"]))
birds.crs = {'init': 'epsg:4326'}

#path
# GeoDataFrame showing path for each bird
path_df = birds.groupby("tag-local-identifier")['geometry'].apply(list).apply(lambda x: LineString(x)).reset_index()
path_gdf = gpd.GeoDataFrame(path_df, geometry=path_df.geometry)
path_gdf.crs = {'init': 'epsg:4326'}

# GeoDataFrame showing starting point for each bird
start_df = birds.groupby("tag-local-identifier")['geometry'].apply(list).apply(lambda x: x[0]).reset_index()
start_gdf = gpd.GeoDataFrame(start_df, geometry=start_df.geometry)
start_gdf.crs = {'init': 'epsg:4326'}

# GeoDataFrame showing ending point for each bird
end_df = birds.groupby("tag-local-identifier")['geometry'].apply(list).apply(lambda x: x[-1]).reset_index()
end_gdf = gpd.GeoDataFrame(end_df, geometry=end_df.geometry)
end_gdf.crs = {'init' :'epsg:4326'}

# protected places
protected_areas= gpd.read_file("C:/Users/TanviMore/Desktop/DataAnalytics/SAPA_Aug2019-shapefile/SAPA_Aug2019-shapefile/SAPA_Aug2019-shapefile-polygons.shp")
P_Area = sum(protected_areas['REP_AREA']-protected_areas['REP_M_AREA'])
print("South America has {} square kilometers of protected areas.".format(P_Area))
totalArea = sum(south_america.geometry.to_crs(epsg=3035).area) / 10**6
print("Total area of South America = ", totalArea)

#plot
ax=america.plot(figsize=(15,15), color='white', linestyle=':', edgecolor='black')
path_gdf.plot(ax=ax, cmap='tab20b', linestyle="-", zorder=1)
start_gdf.plot(ax=ax, color='red',markersize=30)
end_gdf.plot(ax=ax, color='black',markersize=30)
protected_areas.plot(ax=ax,color='blue',alpha=0.4)
plt.show(block=True)
