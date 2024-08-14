import numpy as np
import cv2
import rasterio

def compute_shadow_length(boulder_height, sun_elevation):
    # Convert sun elevation to radians
    elevation_rad = np.radians(sun_elevation)
    # Calculate the shadow length
    shadow_length = boulder_height / np.tan(elevation_rad)
    return shadow_length

def color_shadows(image, shadows):
    # Convert shadows to a 3-channel image (BGR)
    colored_shadows = cv2.cvtColor(shadows, cv2.COLOR_GRAY2BGR)

    # Apply a color to the shadow areas (e.g., blue color)
    colored_shadows[shadows > 0] = [255, 0, 0]  # Blue color

    # Overlay the colored shadows on the original image
    result = cv2.addWeighted(image, 0.7, colored_shadows, 0.3, 0)

    return result

def apply_shading_effect(image, sun_azimuth, sun_elevation, shadow_threshold):
    # Assuming boulder height is known or estimated (example value: 1 meter)
    boulder_height = 1.0  # Example: 1 meter

    # Compute shadow length
    shadow_length = compute_shadow_length(boulder_height, sun_elevation)

    # If shadow length is greater than the threshold, mark it as a boulder
    if shadow_length > shadow_threshold:
        # Assuming shadows are detected (using any method, e.g., edge detection)
        shadows = np.zeros_like(image, dtype=np.uint8)
        shadows[image < 100] = 255  # Example thresholding for shadow detection

        # Color the shadows
        colored_shadows = color_shadows(image, shadows)

        return colored_shadows
    else:
        return image

# Main function to process the image
def process_image(image_path, sun_azimuth, sun_elevation, shadow_threshold):
    # Open the image using Rasterio
    with rasterio.open(image_path) as src:
        image = src.read(1)  # Read the first band (assumed grayscale)

    # Normalize the image for better visualization
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Apply shading effect
    result_image = apply_shading_effect(image, sun_azimuth, sun_elevation, shadow_threshold)

    # Display the result
    cv2.imshow('Colored Shadows', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Sun illumination parameters (example values)
image_path='cropped_image/piece_0.tif'
sun_azimuth = 119.823526  # degrees
sun_elevation = 15.659790  # degrees
shadow_threshold = 5  # Minimum shadow length to be considered a boulder

# Apply shading effect
process_image(image_path, sun_azimuth, sun_elevation, shadow_threshold)
