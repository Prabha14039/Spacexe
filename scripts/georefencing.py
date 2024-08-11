import json
import cv2
import pandas as pd

def pixel_to_lat_lon(pixel, csv_file):
    # Load CSV
    df = pd.read_csv(csv_file)

    # Iterate through the DataFrame rows
    for _, row in df.iterrows():
        # Directly use integer values if they are already correct
        if int(row['Pixel']) == pixel:
            latitude = float(row['Latitude'])
            longitude = float(row['Longitude'])
            print(f'Pixel: {pixel}, Latitude: {latitude}, Longitude: {longitude}')
            return latitude, longitude
    # Return None if no match is found
    return None, None

def draw_bounding_boxes(image_path, json_file, csv_file, output_image_path, output_txt_path):
    # Load the image
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    # Load the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Open the text file to save lat/lon information
    with open(output_txt_path, 'w') as txt_file:
        # Iterate through the predictions in the JSON file
        for obj in data['predictions']:
            # Get bounding box coordinates in pixels
            x_center = obj['x'] * width
            y_center = obj['y'] * height
            bbox_width = obj['width'] * width
            bbox_height = obj['height'] * height

            # Calculate bounding box coordinates
            x1 = int(x_center - bbox_width / 2)
            y1 = int(y_center - bbox_height / 2)
            x2 = int(x_center + bbox_width / 2)
            y2 = int(y_center + bbox_height / 2)

            # Convert pixel coordinates to latitude and longitude
            lat1, lon1 = pixel_to_lat_lon(x1, csv_file)
            lat2, lon2 = pixel_to_lat_lon(x2, csv_file)

            # Draw the bounding box on the image and save details
            if lat1 is not None and lon1 is not None and lat2 is not None and lon2 is not None:
                # Draw the bounding box on the image
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, f'Lat: {lat1}, Lon: {lon1}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                cv2.putText(image, f'Diameter: {int(bbox_width)} px', (x1, y2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                # Save lat/lon info to the text file
                txt_file.write(f'Bounding Box: ({x1}, {y1}) to ({x2}, {y2})\n')
                txt_file.write(f'Lat1: {lat1}, Lon1: {lon1}\n')
                txt_file.write(f'Lat2: {lat2}, Lon2: {lon2}\n')
                txt_file.write(f'Diameter: {int(bbox_width)} px\n')
                txt_file.write('-----------------------------------\n')

    # Save the output image
    cv2.imwrite(output_image_path, image)

# Example usage
image_path = 'images/piece_0.png'  # Path to your image
json_file = 'json/piece_0.json'     # Path to your JSON file with bounding box results
csv_file = 'ch2_ohr_ncp_20230227T0727599533_g_grd_n18.csv'  # Path to your CSV file with pixel to lat/lon mapping
output_image_path = 'output_image_with_boxes.jpg'  # Path to save the image with bounding boxes
output_txt_path = 'bounding_boxes_info.txt'  # Path to save the bounding box information

# Draw bounding boxes and save output
draw_bounding_boxes(image_path, json_file, csv_file, output_image_path, output_txt_path)

