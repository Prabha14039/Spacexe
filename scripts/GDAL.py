import numpy as np
import rasterio
import matplotlib.pyplot as plt
from rasterio.transform import from_origin
import cv2
import xml.etree.ElementTree as ET

# Load the XML file
tree = ET.parse('ch2_ohr_ncp_20230820T0559124374_d_img_n18.xml')

root = tree.getroot()

# Define namespaces to deal with XML namespaces
namespaces = {
    'pds': 'http://pds.nasa.gov/pds4/pds/v1',
    'isda': 'https://isda.issdc.gov.in/pds4/isda/v1'
}

# Find the Axis_Array elements
axis_arrays = root.findall('.//pds:Array_2D_Image/pds:Axis_Array', namespaces)

# Initialize height and width
height = None
width = None

# Extract height and width based on axis_name
for axis in axis_arrays:
    axis_name = axis.find('pds:axis_name', namespaces).text
    elements = int(axis.find('pds:elements', namespaces).text)

    if axis_name == "Line":
        height = elements
    elif axis_name == "Sample":
        width = elements

# Path to the binary image file


# Parameters (update these based on your image's specifications)
binary_file_path = 'ch2_ohr_ncp_20230820T0559124374_d_img_n18.img'
tiff_file_path = 'output_file.tif'
width = 12000   # Replace with the actual width of your image
height = 93692  # Replace with the actual height of your image
dtype = np.uint8  # Data type (e.g., np.uint8 for 8-bit grayscale image)
pixel_size = 0.26  # Pixel resolution in meters (update as needed)

# Step 1: Read binary data
with open(binary_file_path, 'rb') as f:
    binary_data = f.read()

# Step 2: Convert binary data to numpy array and reshape it
image_array = np.frombuffer(binary_data, dtype=dtype).reshape((height, width))

# Step 3: Save the numpy array as a TIFF file
transform = from_origin(0, height * pixel_size, pixel_size, pixel_size)  # Adjust origin and resolution

with rasterio.open(
    tiff_file_path, 'w', driver='GTiff',
    height=image_array.shape[0], width=image_array.shape[1],
    count=1, dtype=image_array.dtype,
    crs='EPSG:4326',  # Set appropriate CRS
    transform=transform
) as dst:
    dst.write(image_array, 1)

# Step 4: Display the TIFF file
with rasterio.open(tiff_file_path) as src:
    image_array = src.read(1)  # Read the first band
    plt.figure(figsize=(10, 10))
    plt.imshow(image_array, cmap='gray')
    plt.colorbar()
    plt.title('Binary Image')
    plt.xlabel('Pixel')
    plt.ylabel('Pixel')
    plt.show()

