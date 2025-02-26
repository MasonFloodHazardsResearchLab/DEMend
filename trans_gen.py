import arcpy
import geopandas as gpd
from shapely.geometry import LineString
import numpy as np
from pathlib import Path

def create_transect(line, length=15):
    mid_point = line.interpolate(0.5, normalized=True)   
    x, y = line.xy
    dx = x[-1] - x[0]
    dy = y[-1] - y[0]
    angle = np.arctan2(dy, dx)  
    start_point = (mid_point.x - (length / 2) * np.cos(angle + np.pi/2), mid_point.y - (length / 2) * np.sin(angle + np.pi/2))
    end_point = (mid_point.x + (length / 2) * np.cos(angle + np.pi/2), mid_point.y + (length / 2) * np.sin(angle + np.pi/2))
    transect = LineString([start_point, end_point])
    return transect

# Get the input parameters
selected_lines_path = arcpy.GetParameterAsText(0)  # Path to the selected lines shapefile
transect_length = float(arcpy.GetParameterAsText(1))  # Length of the transects
output_transects_path = arcpy.GetParameterAsText(2)  # Path to the output transects shapefile


# Read the selected lines shapefile
obs_lines = gpd.read_file(selected_lines_path)

# Filter lines near roads
transects = obs_lines

# Create transects
transects['transect'] = transects['geometry'].apply(create_transect, args=(transect_length,))
transects = transects.drop(columns=['geometry'])
transects = transects.rename(columns={'transect': 'geometry'})

# Save the transects to a new shapefile
transects.to_file(output_transects_path)

# Set the output parameter
arcpy.SetParameterAsText(2, output_transects_path)