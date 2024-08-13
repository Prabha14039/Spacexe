import rasterio

# Path to your TIFF file
tif_path = 'georeferenced_image.tif'

# Open the TIFF file
with rasterio.open(tif_path) as src:
    # Print basic information
    print(f"File Path: {tif_path}")
    print(f"Driver: {src.driver}")
    print(f"Width: {src.width}")
    print(f"Height: {src.height}")
    print(f"Count: {src.count} (Number of bands)")
    print(f"CRS: {src.crs}")
    print(f"Transform: {src.transform}")
    print(f"Bounding Box: {src.bounds}")

    # Read the first band
    band1 = src.read(1)  # Reading the first band
    print(f"Band 1 Shape: {band1.shape}")

    # Optionally, display the image using matplotlib
    import matplotlib.pyplot as plt
    plt.imshow(band1, cmap='gray')
    plt.colorbar()
    plt.title('First Band of TIFF Image')
    plt.show()

