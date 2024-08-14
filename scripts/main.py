import cv2
import numpy as np

def compute_gradient_magnitude_and_direction(image):
    grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

    magnitude = np.sqrt(grad_x*2 + grad_y*2)
    direction = np.arctan2(grad_y, grad_x) * (180 / np.pi) % 180

    return magnitude, direction

def non_max_suppression(magnitude, direction):
    # Perform non-maxima suppression
    h, w = magnitude.shape
    output = np.zeros_like(magnitude, dtype=np.uint8)

    # Directional angles (rounded to nearest 45 degrees)
    direction = direction / 45.0
    direction = np.round(direction) * 45

    for i in range(1, h-1):
        for j in range(1, w-1):
            angle = direction[i, j]
            if angle == 0:  # Horizontal edge
                q = magnitude[i, j+1]
                r = magnitude[i, j-1]
            elif angle == 45:  # Diagonal edge (top-left to bottom-right)
                q = magnitude[i+1, j-1]
                r = magnitude[i-1, j+1]
            elif angle == 90:  # Vertical edge
                q = magnitude[i+1, j]
                r = magnitude[i-1, j]
            elif angle == 135:  # Diagonal edge (top-right to bottom-left)
                q = magnitude[i-1, j-1]
                r = magnitude[i+1, j+1]

            if magnitude[i, j] >= q and magnitude[i, j] >= r:
                output[i, j] = magnitude[i, j]

    return output

### 2. Adjust Thresholding

def compute_histogram_and_thresholds(magnitude):
    hist = cv2.calcHist([magnitude], [0], None, [256], [0, 256])
    hist = hist.flatten()

    gm = np.argmax(hist)
    gamma_m = np.sum((np.arange(256) - gm)**2 * hist) / np.sum(hist)

    Th = gm + np.sqrt(gamma_m) * 0.5  # Fine-tune here
    Tl = max(0, gm - np.sqrt(gamma_m) * 0.5)  # Fine-tune here

    return Th, Tl

### 3. Morphological Post-processing

def apply_morphology(edges):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)
    edges = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel, iterations=2)
    return edges

def adaptive_canny_edge_detection(image):
    magnitude, direction = compute_gradient_magnitude_and_direction(image)
    ridge_image = non_max_suppression(magnitude, direction)
    Th, Tl = compute_histogram_and_thresholds(ridge_image)

    edges = cv2.Canny(image, Tl, Th)
    edges = apply_morphology(edges)

    return edges

image_path = 'cropped_image/piece_0.tif'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
edges = adaptive_canny_edge_detection(image)

cv2.imshow('EDGES',edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
