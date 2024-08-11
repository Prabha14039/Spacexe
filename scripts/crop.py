from PIL import Image
import os

def crop_image(input_path, output_dir, crop_size=(1200, 1200)):
    # Open the image file
    with Image.open(input_path) as img:
        img_width, img_height = img.size
        crop_width, crop_height = crop_size

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Crop the image into multiple pieces
        piece_count = 0
        for top in range(0, img_height, crop_height):
            for left in range(0, img_width, crop_width):
                # Define the box to crop
                box = (left, top, left + crop_width, top + crop_height)
                # Crop and save the image piece
                img_cropped = img.crop(box)
                piece_filename = os.path.join(output_dir, f'piece_{piece_count}.png')
                img_cropped.save(piece_filename)
                piece_count += 1

# Example usage
input_image_path = 'ch2_ohr_ncp_20230227T0727599533_b_brw_n18.png'
output_directory = 'images'
crop_image(input_image_path, output_directory)
