import numpy as np
import matplotlib.pyplot as plt
import rasterio
from matplotlib.patches import Polygon
from rasterio.transform import from_origin

# Define the corner coordinates from XML (in degrees)
bounding_boxes = [
    {
        'upper_left_lat': -2.576048,
        'upper_left_lon': 336.486234,
        'upper_right_lat': -2.579083,
        'upper_right_lon': 336.589455,
        'lower_left_lat': -3.413866,
        'lower_left_lon': 336.484646,
        'lower_right_lat': -3.416904,
        'lower_right_lon': 336.587773
    }
]

# Load the georeferenced TIFF image
image_path = 'georeferenced_image.tif'
with rasterio.open(image_path) as src:
    image_array = src.read(1)  # Read the first band
    transform = src.transform
    crs = src.crs

# Plot the image
plt.figure(figsize=(12, 8))
plt.imshow(image_array, cmap='gray', origin='upper')
plt.title('Georeferenced OHRC Image')

# Overlay the bounding boxes
for box in bounding_boxes:
    # Convert coordinates from degrees to pixel coordinates
    upper_left = ~transform * (box['upper_left_lon'], box['upper_left_lat'])
    upper_right = ~transform * (box['upper_right_lon'], box['upper_right_lat'])
    lower_left = ~transform * (box['lower_left_lon'], box['lower_left_lat'])
    lower_right = ~transform * (box['lower_right_lon'], box['lower_right_lat'])

    # Print the coordinates for debugging
    print(f"Upper left pixel: {upper_left}")
    print(f"Upper right pixel: {upper_right}")
    print(f"Lower left pixel: {lower_left}")
    print(f"Lower right pixel: {lower_right}")

    # Create a polygon for the bounding box
    polygon = Polygon([
        (upper_left[0], upper_left[1]),
        (upper_right[0], upper_right[1]),
        (lower_right[0], lower_right[1]),
        (lower_left[0], lower_left[1])
    ], closed=True, edgecolor='red', fill=None, linewidth=2)

    # Add the polygon to the plot
    plt.gca().add_patch(polygon)

plt.colorbar()
plt.show()
