import rasterio
import matplotlib.pyplot as plt
import numpy as np

# Path to your TIFF file
tif_path = 'georeferenced_image.tif'

# Open the TIFF file
with rasterio.open(tif_path) as src:
    # Read the first band
    band1 = src.read(1)

    # Get the image dimensions
    height, width = band1.shape

    # Set up the plot
    fig, ax = plt.subplots(figsize=(10, 10))
    cax = ax.imshow(band1, cmap='gray', origin='upper')
    plt.colorbar(cax, ax=ax, orientation='vertical', label='Pixel Value')
    ax.set_title('TIFF Image with Pixel Grid')

    # Add gridlines
    ax.set_xticks(np.arange(0, width, step=100), minor=True)  # Adjust step as needed
    ax.set_yticks(np.arange(0, height, step=100), minor=True) # Adjust step as needed
    ax.grid(which='minor', color='r', linestyle='--', linewidth=0.5)

    # Label the gridlines
    ax.set_xticks(np.arange(0, width, step=100))  # Adjust step as needed
    ax.set_yticks(np.arange(0, height, step=100)) # Adjust step as needed
    ax.set_xticklabels(np.arange(0, width, step=100))  # Adjust step as needed
    ax.set_yticklabels(np.arange(0, height, step=100)) # Adjust step as needed

    # Show the plot
    plt.show()

