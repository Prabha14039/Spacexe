import os
import json
from roboflow import Roboflow

# Initialize Roboflow client
api_key = "jI9zPooZS2V3AFXS4jRh"
rf = Roboflow(api_key=api_key)
project = rf.workspace().project("lunar-crater-detection-2")
model = project.version(2).model

def perform_inference(image_path, confidence, overlap):
    """
    Perform inference on an image using the Roboflow model and return the result as JSON.

    Parameters:
    - image_path: str, path to the input image
    - confidence: int, minimum confidence threshold (percentage)
    - overlap: int, overlap threshold (percentage)

    Returns:
    - dict, inference result in JSON format
    """
    try:
        result = model.predict(image_path, confidence=confidence, overlap=overlap).json()
        return result
    except Exception as e:
        print(f"Error during inference for {image_path}: {e}")
        return None

def process_directory(input_dir, output_dir, confidence=10, overlap=40):
    """
    Process all images in a directory, perform inference, and save results as JSON files.

    Parameters:
    - input_dir: str, path to the directory containing input images
    - output_dir: str, path to the directory where JSON files will be saved
    - confidence: int, minimum confidence threshold (percentage)
    - overlap: int, overlap threshold (percentage)
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process each image in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.tif','.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_dir, filename)
            json_filename = os.path.splitext(filename)[0] + '.json'
            output_json_path = os.path.join(output_dir, json_filename)

            print(f"Processing {image_path}...")
            result = perform_inference(image_path, confidence, overlap)

            if result:
                # Save the result as a JSON file
                with open(output_json_path, 'w') as json_file:
                    json.dump(result, json_file, indent=4)
                print(f"Inference result saved to {output_json_path}")

if __name__ == "__main__":
    # Specify the input and output directories
    #input_dir = "../images/train"  # Replace with the path to your image directory
    input_dir = "cropped_image"  # Replace with the path to your image directory
    output_dir = "json"  # Replace with the path to save JSON files

    # Process the directory
    process_directory(input_dir, output_dir, confidence=10, overlap=40)

