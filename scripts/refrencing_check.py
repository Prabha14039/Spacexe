import os
import json
import cv2

def draw_boxes_on_image(image_path, json_path, output_path):
    """
    Draw bounding boxes from JSON file on the image and save the annotated image.

    Parameters:
    - image_path: str, path to the input image
    - json_path: str, path to the JSON file with bounding box information
    - output_path: str, path to save the annotated image
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error loading image {image_path}")
        return

    # Load the JSON data
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Iterate over the objects in the JSON data
    for obj in data.get('predictions', []):
        x, y, w, h = obj['x'], obj['y'], obj['width'], obj['height']
        # Convert coordinates to bounding box format (x1, y1, x2, y2)
        x1, y1 = int(x - w / 2), int(y - h / 2)
        x2, y2 = int(x + w / 2), int(y + h / 2)

        # Draw the bounding box on the image
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Save the annotated image
    cv2.imwrite(output_path, image)
    print(f"Annotated image saved to {output_path}")

def process_directory(input_images_dir, input_jsons_dir, output_dir):
    """
    Process images and their corresponding JSON files, and save annotated images.

    Parameters:
    - input_images_dir: str, path to the directory containing input images
    - input_jsons_dir: str, path to the directory containing JSON files
    - output_dir: str, path to save annotated images
    """
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through images and corresponding JSON files
    for filename in os.listdir(input_images_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_images_dir, filename)
            json_filename = os.path.splitext(filename)[0] + '.json'
            json_path = os.path.join(input_jsons_dir, json_filename)
            output_image_path = os.path.join(output_dir, filename)

            if os.path.exists(json_path):
                print(f"Processing {image_path} with {json_path}...")
                draw_boxes_on_image(image_path, json_path, output_image_path)
            else:
                print(f"JSON file not found for {image_path}")

if __name__ == "__main__":
    # Directories
    input_images_dir = "../images/train"  # Replace with the path to your image directory
    input_jsons_dir = "json"  # Replace with the path to your JSON files
    output_dir = "annotated_images"  # Replace with the path to save annotated images

    # Process the directory
    process_directory(input_images_dir, input_jsons_dir, output_dir)

