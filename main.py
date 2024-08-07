import numpy as np
import matplotlib.pyplot as plt
from rasterio.transform import from_origin
import rasterio

# Define the parameters
num_lines = 93693
num_samples = 12000
pixel_resolution = 0.24746317230036705  # meters per pixel

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pyproj import Proj, Transformer
from rasterio.transform import from_origin
import rasterio

# Paths to the files
img_path = '/home/prabha03/work/hackathon/ch2_ohr_ncp_36730/data/calibrated/20210405/ch2_ohr_ncp_20210405T1606536730_d_img_d18.img'
csv_path = '/home/prabha03/work/hackathon/ch2_ohr_ncp_36730/geometry/calibrated/20210405/ch2_ohr_ncp_20210405T1606536730_g_grd_d18.csv'
tiff_path = 'georeferenced_image.tif'

# Image parameters
upper_left_lat = -2.576048
upper_left_lon = 336.486234
pixel_resolution = 0.24746317230036705  # meters/pixel
num_lines = 93693
num_samples = 12000

# Load the image
image_data = np.fromfile(img_path, dtype=np.uint8)
image_array = image_data.reshape((num_lines, num_samples))

# Create a transform for the image
transform = from_origin(upper_left_lon, upper_left_lat, pixel_resolution, pixel_resolution)

# Write the georeferenced image
with rasterio.open(tiff_path, 'w', driver='GTiff',
                   height=image_array.shape[0], width=image_array.shape[1],
                   count=1, dtype='uint8', crs='EPSG:4326', transform=transform) as dst:
    dst.write(image_array, 1)

# Load CSV data
csv_data = pd.read_csv(csv_path)
longitudes = csv_data['Longitude'].values
latitudes = csv_data['Latitude'].values
pixels = csv_data['Pixel'].values
scans = csv_data['Scan'].values

# Define the projection for conversion
proj_wgs84 = Proj(init='epsg:4326')  # WGS84
# Use the appropriate UTM zone or projection for your data
proj_img = Proj(proj='utm', zone=33, datum='WGS84')  # Example UTM projection
transformer = Transformer.from_proj(proj_wgs84, proj_img, always_xy=True)

# Convert coordinates to image pixel coordinates
def lat_lon_to_pixel(lat, lon, transform, width, height):
    px, py = transform.transform(lon, lat)
    x = int(px)
    y = height - int(py)
    return x, y

# Convert all coordinates
image_width = num_samples
image_height = num_lines
pixel_coords = [lat_lon_to_pixel(lat, lon, transformer, image_width, image_height) for lat, lon in zip(latitudes, longitudes)]

# Plot the image with bounding boxes
with rasterio.open(tiff_path) as src:
    image_array = src.read(1)

fig, ax = plt.subplots()
ax.imshow(image_array, cmap='gray')

# Draw bounding boxes
for i in range(0, len(pixel_coords), 4):
    if i + 3 >= len(pixel_coords):
        break
    # Example coordinates for bounding box; modify as needed
    upper_left = pixel_coords[i]
    upper_right = pixel_coords[i+1]
    lower_right = pixel_coords[i+2]
    lower_left = pixel_coords[i+3]

    # Create a rectangle
    rect = patches.Polygon([upper_left, upper_right, lower_right, lower_left], linewidth=2, edgecolor='r', facecolor='none')
    ax.add_patch(rect)

plt.title('Georeferenced OHRC Image with Bounding Boxes')
plt.show()

