import rasterio
import json
import os
from rasterio.transform import from_origin

# Properties used in the original TIFF creation
dtype = 'uint8'  # Data type (e.g., np.uint8 for 8-bit grayscale image)
pixel_size = 0.26  # Pixel resolution in meters

def crop_image(input_path, output_dir, crop_size=(1200, 1200)):
    with rasterio.open(input_path) as src:
        img_width, img_height = src.width, src.height
        crop_width, crop_height = crop_size

        os.makedirs(output_dir, exist_ok=True)

        piece_count = 0
        metadata = []

        for top in range(0, img_height, crop_height):
            for left in range(0, img_width, crop_width):
                box = (left, top, min(left + crop_width, img_width), min(top + crop_height, img_height))
                window = rasterio.windows.Window(left, top, box[2] - box[0], box[3] - box[1])

                # Read the data from the window
                data = src.read(window=window)

                # Save the crop metadata
                piece_filename = os.path.join(output_dir, f'piece_{piece_count}.tif')
                metadata.append({
                    'filename': piece_filename,
                    'left': left,
                    'top': top
                })

                # Write the cropped data to a new GeoTIFF file
                with rasterio.open(
                    piece_filename,
                    'w',
                    driver='GTiff',
                    height=data.shape[1],
                    width=data.shape[2],
                    count=src.count,
                    dtype=dtype,
                    crs=src.crs,
                    transform=from_origin(left * pixel_size, (img_height - top) * pixel_size, pixel_size, pixel_size)
                ) as dst:
                    dst.write(data)

                piece_count += 1

        # Save metadata to a JSON file
        with open(os.path.join(output_dir, 'metadata.json'), 'w') as f:
            json.dump(metadata, f)

# Example usage
input_image_path = 'main.tif'
output_directory = 'cropped_image'
crop_image(input_image_path, output_directory)

