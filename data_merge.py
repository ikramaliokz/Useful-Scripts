""" 
    if you want to merge the classification dataset. like two different images dataset with same classes
    you may use this script 
"""

import os
import shutil

# Define the paths to your datasets and the path for the merged dataset
dataset1_path = '/home/athenaai/Desktop/Lego/RealImagesTest/train'
dataset2_path = '/home/athenaai/Desktop/Lego/test/train'
merged_dataset_path = '/home/athenaai/Desktop/Lego/MixedDataset/train'

# Create the merged dataset directory if it doesn't exist
if not os.path.exists(merged_dataset_path):
    os.makedirs(merged_dataset_path)

# Function to copy and rename files to avoid overwriting
def copy_and_rename(src, dst):
    file_name, file_extension = os.path.splitext(os.path.basename(src))
    counter = 1
    new_file_name = file_name + file_extension
    new_dst = os.path.join(dst, new_file_name)

    while os.path.exists(new_dst):
        new_file_name = f"{file_name}_{counter}{file_extension}"
        new_dst = os.path.join(dst, new_file_name)
        counter += 1

    shutil.copy2(src, new_dst)

# Copy files from both datasets to the merged dataset
for class_folder in os.listdir(dataset1_path):
    class_folder_path1 = os.path.join(dataset1_path, class_folder)
    class_folder_path2 = os.path.join(dataset2_path, class_folder)
    merged_class_folder_path = os.path.join(merged_dataset_path, class_folder)

    # Create class folder in merged dataset
    if not os.path.exists(merged_class_folder_path):
        os.makedirs(merged_class_folder_path)

    # Copy from dataset 1
    for file in os.listdir(class_folder_path1):
        file_path = os.path.join(class_folder_path1, file)
        copy_and_rename(file_path, merged_class_folder_path)

    # Copy from dataset 2
    for file in os.listdir(class_folder_path2):
        file_path = os.path.join(class_folder_path2, file)
        copy_and_rename(file_path, merged_class_folder_path)

print("Merging complete.")
