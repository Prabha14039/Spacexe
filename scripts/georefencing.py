import pandas as pd
import numpy as np
from scipy.optimize import least_squares
import rasterio
from rasterio.transform import from_origin, Affine

# Load the CSV file
df = pd.read_csv('ch2_ohr_ncp_20230820T0559124374_g_grd_n18.csv')

# Extract coordinates and pixel locations
longitudes = df['Longitude'].values
latitudes = df['Latitude'].values
x_pixels = df['Pixel'].values
y_pixels = df['Scan'].values

# Convert coordinates to numpy arrays
coords = np.array([longitudes, latitudes]).T
pixels = np.array([x_pixels, y_pixels]).T

# Define a function to compute residuals for least squares fitting
def residuals(params, coords, pixels):
    # Transformation parameters
    a, b, c, d, e, f = params
    # Transform pixel coordinates to georeferenced coordinates
    predicted_coords = np.dot(pixels, np.array([[a, b], [d, e]])) + np.array([c, f])
    return np.concatenate((predicted_coords[:, 0] - coords[:, 0], predicted_coords[:, 1] - coords[:, 1]))

# Initial guess for transformation parameters
initial_guess = [1, 0, 0, 0, 1, 0]

# Solve for transformation parameters
result = least_squares(residuals, initial_guess, args=(coords, pixels))

# Extract transformation parameters
a, b, c, d, e, f = result.x

# Create the affine transformation matrix
transform = Affine(a, b, c, d, e, f)

# Open the existing TIFF file
with rasterio.open('output_file.tif') as src:
    profile = src.profile

    # Update the profile with new CRS and transformation
    profile.update({
        'crs': 'EPSG:4326',  # Assuming your image uses EPSG:4326; adjust if necessary
        'transform': transform
    })

    # Write out the georeferenced file
    with rasterio.open('georeferenced_image.tif', 'w', **profile) as dst:
        dst.write(src.read())

print("Georeferencing complete.")

