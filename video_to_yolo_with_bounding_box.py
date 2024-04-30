import cv2
import os
import numpy as np

def extract_frames(video_path, output_folder, skip_frames=0):
    """
    Extract frames from a video file.
    Args:
    - video_path: Path to the video file.
    - output_folder: Folder where extracted frames will be saved.
    - skip_frames: Number of frames to skip between extractions.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0
    while success:
        if count % (skip_frames + 1) == 0:
            cv2.imwrite(f"{output_folder}/frame{count}.jpg", image)
        success, image = vidcap.read()
        count += 1
    vidcap.release()

def find_bounding_boxes(mask_path):
    """
    Find bounding boxes from a mask image.
    Args:
    - mask_path: Path to the mask image.
    Returns:
    - A list of bounding boxes in the format (x1, y1, x2, y2).
    """
    mask = cv2.imread(mask_path, 0)
    ret, thresh = cv2.threshold(mask, 127, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    bounding_boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        bounding_boxes.append((x, y, x+w, y+h))
    return bounding_boxes

def write_yolo_annotations(bounding_boxes, output_path, img_width, img_height):
    """
    Write YOLO formatted annotations to a file.
    Args:
    - bounding_boxes: List of bounding boxes for objects in the image.
    - output_path: Path to save the annotation file.
    - img_width: Width of the image.
    - img_height: Height of the image.
    """
    with open(output_path, 'w') as f:
        for (x1, y1, x2, y2) in bounding_boxes:
            x_center = ((x1 + x2) / 2) / img_width
            y_center = ((y1 + y2) / 2) / img_height
            width = (x2 - x1) / img_width
            height = (y2 - y1) / img_height
            # Assuming '0' is the class index for potholes
            f.write(f"0 {x_center} {y_center} {width} {height}\n")

def prepare_dataset(real_video_path, mask_video_path, output_images_folder, output_labels_folder, skip_frames=0):
    """
    Prepare the dataset for YOLO model training with segmentation masks.
    Args:
    - real_video_path: Path to the real video.
    - mask_video_path: Path to the mask video.
    - output_images_folder: Folder to save extracted frames from the real video.
    - output_labels_folder: Folder to save YOLO formatted annotations.
    - skip_frames: Number of frames to skip between extractions.
    """
    extract_frames(real_video_path, output_images_folder, skip_frames)
    extract_frames(mask_video_path, output_labels_folder, skip_frames)  # Temporary, for masks
    
    for frame_name in os.listdir(output_images_folder):
        mask_path = os.path.join(output_labels_folder, frame_name)
        if os.path.exists(mask_path):
            img_path = os.path.join(output_images_folder, frame_name)
            img = cv2.imread(img_path)
            img_height, img_width = img.shape[:2]
            bounding_boxes = find_bounding_boxes(mask_path)
            annotation_path = os.path.join(output_labels_folder, frame_name.replace('.jpg', '.txt'))
            write_yolo_annotations(bounding_boxes, annotation_path, img_width, img_height)
            os.remove(mask_path)  # Remove mask frame after processing

# Example usage
real_video_path = 'pothole_video/test/mask/0081.mp4'
mask_video_path = 'pothole_video/test/rgb/0081.mp4'
output_images_folder = 'output/images'
output_labels_folder = 'output/labels'

prepare_dataset(real_video_path, mask_video_path, output_images_folder, output_labels_folder, skip_frames=5)
