import rasterio
import json
import os

def recombine_image(crop_dir, output_path):
    # Load metadata
    with open(os.path.join(crop_dir, 'metadata.json'), 'r') as f:
        metadata = json.load(f)

    # Load one piece to get dimensions
    first_piece = rasterio.open(metadata[0]['filename'])
    crop_width, crop_height = first_piece.width, first_piece.height

    # Determine original image size
    original_width = max(item['left'] + crop_width for item in metadata)
    original_height = max(item['top'] + crop_height for item in metadata)

    # Create a new GeoTIFF image with the original dimensions
    with rasterio.open(
        output_path,
        'w',
        driver='GTiff',
        height=original_height,
        width=original_width,
        count=first_piece.count,
        dtype=first_piece.dtypes[0],
        crs=first_piece.crs,
        transform=rasterio.Affine.identity()  # Adjust transform as needed
    ) as dst:
        # Initialize an empty array for combining pieces
        for item in metadata:
            piece = rasterio.open(item['filename'])
            window = rasterio.windows.Window(
                item['left'],
                item['top'],
                piece.width,
                piece.height
            )
            # Read data from each piece and write it to the new image
            data = piece.read(window=window)
            dst.write(data, indexes=range(1, first_piece.count + 1), window=window)

    print(f"Recombined image saved to {output_path}")

# Example usage
crop_directory = 'cropped_images'
output_image_path = 'ecombined_image.tif'
recombine_image(crop_directory, output_image_path)

