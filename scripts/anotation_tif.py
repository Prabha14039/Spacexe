import os
import rasterio
from PIL import Image, ImageDraw
import json
import numpy as np

# Load the GeoTIFF image
def load_geotiff(image_path):
    with rasterio.open(image_path) as src:
        count = src.count  # Number of bands
        if count == 1:
            image_array = src.read(1)  # Read the single band
            image_array = np.stack([image_array] * 3, axis=-1)  # Convert to RGB by stacking the single band
        else:
            image_array = src.read([1, 2, 3])  # Read RGB bands if available
            image_array = np.moveaxis(image_array, 0, -1)  # Convert to HxWxC
        return image_array

# Convert numpy array to PIL Image
def array_to_pil(image_array):
    if image_array.shape[2] == 1:
        # Convert grayscale to RGB
        image_array = np.concatenate([image_array] * 3, axis=-1)
    return Image.fromarray(image_array)

# Load the JSON file
def load_json(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

def draw_bounding_boxes(image, boxes, x_offset=0, y_offset=0):
    draw = ImageDraw.Draw(image)
    for box in boxes:
        x = box['x'] + x_offset
        y = box['y'] + y_offset
        width = box['width']
        height = box['height']
        draw.rectangle([x, y, x + width, y + height], outline='red', width=2)
    return image

# Process all images and annotations
def process_images_and_annotations(image_dir, json_dir, output_dir):
    for filename in os.listdir(image_dir):
        if filename.endswith('.tif'):
            image_path = os.path.join(image_dir, filename)
            json_path = os.path.join(json_dir, filename.replace('.tif', '.json'))
            output_path = os.path.join(output_dir, filename.replace('.tif', '_annotated.tif'))

            if os.path.exists(json_path):
                print(f'Processing {filename}')

                # Load image and JSON data
                image_array = load_geotiff(image_path)
                image = array_to_pil(image_array)
                data = load_json(json_path)

                # Assuming JSON file contains a list of boxes directly
                boxes = data.get('predictions', [])  # Adjust if your JSON format is different

                # Draw bounding boxes on the image
                image_with_boxes = draw_bounding_boxes(image, boxes, x_offset=-50, y_offset=-50)

                # Save the annotated image in TIFF format
                image_with_boxes.save(output_path, format='TIFF')
                print(f'Saved annotated image to {output_path}')
            else:
                print(f'No JSON file found for {filename}')

image_dir = 'cropped_image'
json_dir = 'json'
output_dir = 'annotated_image'
process_images_and_annotations(image_dir, json_dir, output_dir)

