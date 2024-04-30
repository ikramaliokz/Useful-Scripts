import cv2
import os

def video_to_frames(video_path, mask_path, output_dir_real, output_dir_mask,vid_count, skip_frames=0):
    # Ensure the output directories exist
    if not os.path.exists(output_dir_real):
        os.makedirs(output_dir_real)
    if not os.path.exists(output_dir_mask):
        os.makedirs(output_dir_mask)

    # Process real video
    vidcap_real = cv2.VideoCapture(video_path)
    success_real, image_real = vidcap_real.read()
    count = 0
    while success_real:
        if count % (skip_frames + 1) == 0:
            cv2.imwrite(os.path.join(output_dir_real, f"val_{vid_count}_{count}.jpg"), image_real)     
        success_real, image_real = vidcap_real.read()
        count += 1
    print(f'Finished processing real video: {video_path}')

    # Process mask video
    vidcap_mask = cv2.VideoCapture(mask_path)
    success_mask, image_mask = vidcap_mask.read()
    count = 0
    while success_mask:
        if count % (skip_frames + 1) == 0:
            cv2.imwrite(os.path.join(output_dir_mask, f"val_{vid_count}_{count}.jpg"), image_mask)     
        success_mask, image_mask = vidcap_mask.read()
        count += 1
    print(f'Finished processing mask video: {mask_path}')

# Directories
dataset_dir = "pothole_video/val"
video_dir = os.path.join(dataset_dir, "rgb")
mask_dir = os.path.join(dataset_dir, "mask")
output_dir = "output/val"
count_of_vid = 0
# Iterate over videos and find corresponding masks
for video_name in os.listdir(video_dir):
    if video_name.endswith(".mp4"):  # Check if it's a video file
        video_path = os.path.join(video_dir, video_name)
        mask_path = os.path.join(mask_dir, video_name)  # Assuming mask has same name

        # Define output directories for frames
        output_dir_real = os.path.join(output_dir, "rgb")
        output_dir_mask = os.path.join(output_dir, "mask")

        video_to_frames(video_path, mask_path, output_dir_real, output_dir_mask, count_of_vid, skip_frames=5)
        count_of_vid+=1