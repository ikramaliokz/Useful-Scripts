"""
    If you have masks of images, you can make yolo segmentation dataset using this script
    Yolo Segmentation Dataset contain images in one folder and its corresponding labels in .txt in another folder
    The labels contain: <class id> <normalized segmentation points (that may be a polygon of the segment)>  
"""


import os
import cv2
from PIL import Image

def get_normalized_polygons_from_mask(mask_path, img_width, img_height):
    # Read the mask
    mask = cv2.imread(mask_path, 0)
    # Threshold the mask to binarize
    ret, thresh = cv2.threshold(mask, 127, 255, 0)
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    normalized_polygons = []
    for contour in contours:
        # Approximate contour to polygon
        epsilon = 0.001 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Normalize and flatten list
        normalized_polygon = [(point[0][0] / img_width, point[0][1] / img_height) for point in approx]
        normalized_polygons.append(normalized_polygon)
    
    return normalized_polygons




output_folder = 'output/val/labels/'  # Adjust as necessary for your output path
os.makedirs(output_folder, exist_ok=True)

for image_filename in os.listdir('dataset/val/rgb'):
    image_path = os.path.join('dataset/val/rgb', image_filename)
    mask_path = os.path.join('dataset/val/mask', image_filename) # Adjust as necessary for mask format

    # Add image information
    with Image.open(image_path) as img:
        width, height = img.size

    # Use get_normalized_polygons_from_mask to get segmentation polygons
    normalized_polygons = get_normalized_polygons_from_mask(mask_path, width, height)

    # Write polygons to file
    label_filename = os.path.splitext(image_filename)[0] + '.txt'
    with open(os.path.join(output_folder, label_filename), 'w') as label_file:
        for polygon in normalized_polygons:
            # Each line in the label file will represent a polygon
            # For segmentation, class_id is followed by the normalized polygon points
            class_id = 0  # Assuming '0' is the class ID for pothole
            polygon_str = ' '.join([f'{p[0]:.6f} {p[1]:.6f}' for p in polygon])
            label_file.write(f'{class_id} {polygon_str}\n')


## For Visualizing the yolo dataset

from PIL import Image, ImageDraw

def draw_polygons_on_image(image_path, label_path):
    # Load the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    img_width, img_height = image.size

    # Open the corresponding label file and draw each polygon
    with open(label_path, 'r') as file:
        for line in file:
            # Parse the line
            parts = line.strip().split(' ')
            class_id = parts[0]  # Not used here, but necessary if handling multiple classes
            points = [tuple(map(float, p.split(' '))) for p in parts[1:]]  # List of (x, y) tuples
            
            # Denormalize points
            denormalized_points = [(x * img_width, y * img_height) for x, y in points]

            # Draw polygon
            draw.polygon(denormalized_points, outline='red')

    return image


## Uncomment for visulaiztion

# Specify the paths to your images and labels
# images_folder = 'dataset/test/rgb'
# labels_folder = 'output/test/labels'

# # Iterate over each image and its corresponding label file
# for image_filename in os.listdir(images_folder):
#     base_filename = os.path.splitext(image_filename)[0]
#     image_path = os.path.join(images_folder, image_filename)
#     label_path = os.path.join(labels_folder, base_filename + '.txt')

#     # Only proceed if the label file exists
#     if os.path.exists(label_path):
#         result_image = draw_polygons_on_image(image_path, label_path)
#         # Display the result or save it
#         # result_image.show()
#         os.makedirs('output/visualization', exist_ok=True)

#         result_image.save(os.path.join('output/visualization', image_filename))  # Optionally save the result


