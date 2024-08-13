import rasterio
import matplotlib.pyplot as plt

# Path to your TIFF file
tif_file_path = 'output.tif'

# Open the TIFF file
with rasterio.open(tif_file_path) as src:
    # Read the image data as an array
    image_array = src.read(1)  # Reading the first band

    # Flatten the array and filter out any zero values if needed
    image_array = image_array.flatten()

    # Plot the histogram
    plt.figure(figsize=(10, 6))
    plt.hist(image_array, bins=256, range=(0, 256), density=True, color='gray', alpha=0.75)
    plt.title('Histogram of Pixel Values')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

