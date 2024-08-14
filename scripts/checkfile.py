import rasterio
import matplotlib.pyplot as plt

# Path to your GeoTIFF file
geo_tiff_path = 'annotated_image/piece_3_annotated.tif'

# Open the GeoTIFF file
with rasterio.open(geo_tiff_path) as src:
    # Read the image data as an array
    image_array = src.read(1)  # Reading the first band

    # Plot the image
    plt.figure(figsize=(80, 80))
    plt.imshow(image_array, cmap='gray')
    plt.colorbar()
    plt.title('GeoTIFF Image')
    plt.xlabel('Pixel')
    plt.ylabel('Pixel')
    plt.show()

