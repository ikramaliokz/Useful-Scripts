
# For copying less accuracy folders.
import os
import cv2
import shutil
import numpy as np
from PIL import Image

def copy_folders_with_files(path_to_source,source_folders, destination_folder):
    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Iterate through each source folder
    for source_folder in source_folders:
        try:
            # Copy the entire folder including its contents to the destination folder
            shutil.copytree(os.path.join(path_to_source,source_folder), os.path.join(destination_folder, os.path.basename(source_folder)))

            print(f"Folder '{source_folder}' and its contents copied to '{destination_folder}' successfully.")
        except Exception as e:
            print(f"Error copying folder '{source_folder}': {e}")



def copy_folders_with_files(source_folders, destination_folder):
    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Iterate through each source folder
    for source_folder in source_folders:
        try:
            # Copy the entire folder including its contents to the destination folder
            shutil.copytree(source_folder, os.path.join(destination_folder, os.path.basename(source_folder)))

            print(f"Folder '{source_folder}' and its contents copied to '{destination_folder}' successfully.")
        except Exception as e:
            print(f"Error copying folder '{source_folder}': {e}")




def delete_folders(folder_list):
    for folder in folder_list:
        try:
            shutil.rmtree(folder)
            print(f"Folder '{folder}' and its contents deleted successfully.")
        except OSError as e:
            print(f"Error deleting folder '{folder}': {e}")



def copy_files_to_destination(src_folders, dest_folder):
    for src_folder in src_folders:
        try:
            # Get the list of files in the source folder
            files = [f for f in os.listdir(src_folder) if os.path.isfile(os.path.join(src_folder, f))]

            # Create the destination folder if it doesn't exist
            os.makedirs(dest_folder, exist_ok=True)

            # Get the name of the source folder
            folder_name = os.path.basename(src_folder)

            # Copy each file to the destination folder with the folder name prefixed
            for file in files:
                src_path = os.path.join(src_folder, file)
                # New filename with folder name prefixed
                new_file_name = f"{folder_name}_{file}"
                dest_path = os.path.join(dest_folder, new_file_name)
                shutil.copy2(src_path, dest_path)
                print(f"File '{file}' from '{src_folder}' renamed to '{new_file_name}' and copied to '{dest_folder}' successfully.")
        except Exception as e:
            print(f"Error copying files from '{src_folder}': {e}")


def copy_images(source_dir, destination_dir):
    """
    Copies image files from the source directory and its subdirectories to the destination directory.

    Args:
        source_dir (str): Path to the source directory.
        destination_dir (str): Path to the destination directory.
    """

    image_extensions = {".jpg", ".jpeg", ".png", ".gif"}

    for root, _, files in os.walk(source_dir):
        for file in files:
            filepath = os.path.join(root, file)
            _, ext = os.path.splitext(filepath)
            if ext.lower() in image_extensions:
                dest_filepath = os.path.join(destination_dir, file)
                os.makedirs(os.path.dirname(dest_filepath), exist_ok=True)
                shutil.copy2(filepath, dest_filepath)
                print(f"Copied image: {filepath} to {dest_filepath}")


def add_padding_and_resize(input_folder, output_folder, target_size=(640, 640)):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through each file in the input folder
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        try:
            # Read the image using OpenCV
            img = cv2.imread(input_path)
            height1, width1 = img.shape[:2]
            # Get the current dimensions of the image
            smaller_size = (height1//2,width1 //2)
            img = cv2.resize(img, smaller_size)
            height, width = img.shape[:2]

            # Calculate the padding needed on both sides
            padding_top = (target_size[0] - height) // 2
            padding_bottom = target_size[0] - height - padding_top
            padding_left = (target_size[1] - width) // 2
            padding_right = target_size[1] - width - padding_left

            # Add white padding to the image
            padded_img = cv2.copyMakeBorder(img, padding_top, padding_bottom, padding_left, padding_right, cv2.BORDER_CONSTANT, value=[255, 255, 255])

            # Resize the image to the target size
            resized_img = cv2.resize(padded_img, target_size)
            # Convert the image to grayscale
            grayscale_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
            # Save the padded and resized image
            cv2.imwrite(output_path, grayscale_img)
            print(f"Image '{filename}' padded and resized to {target_size}, saved to '{output_folder}' successfully.")

        except Exception as e:
            print(f"Error processing '{filename}': {e}")


# using CV2
def convert_images_to_grayscale(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through each file in the input folder
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        try:
            # Read the image using OpenCV
            img = cv2.imread(input_path)

            # Convert the image to grayscale
            grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Save the grayscale image
            cv2.imwrite(output_path, grayscale_img)
            print(f"Image '{filename}' converted to grayscale and saved to '{output_folder}' successfully.")

        except Exception as e:
            print(f"Error processing '{filename}': {e}")


# using PIL
def convert_images_to_grayscale(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through each file in the input folder
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        try:
            # Open the image
            with Image.open(input_path) as img:
                # Convert the image to grayscale
                grayscale_img = img.convert("L")

                # Save the grayscale image
                grayscale_img.save(output_path)
                print(f"Image '{filename}' converted to grayscale and saved to '{output_folder}' successfully.")

        except Exception as e:
            print(f"Error processing '{filename}': {e}")



def analyze_image_sizes(directory):
    sizes = []
    for dir in os.listdir(directory):
        for filename in os.listdir(directory+dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                try:
                    with Image.open(os.path.join(directory,dir, filename)) as img:
                        sizes.append(img.size)  # img.size is a tuple (width, height)
                except IOError:
                    print(f"Error opening {filename}")

    if not sizes:
        return "No images found or readable."

    # Calculating min, max, and average sizes
    min_size = min(sizes, key=lambda x: x[0]*x[1])
    max_size = max(sizes, key=lambda x: x[0]*x[1])
    avg_size = tuple(sum(x) / len(sizes) for x in zip(*sizes))

    return {
        'Range of Sizes': sizes,
        'Min Size': min_size,
        'Max Size': max_size,
        'Average Size': avg_size
    }


def preprocess_image(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Resize the image
    image = cv2.resize(image, (400, 400))  # Adjust the size as needed

    # Apply Gaussian Blur
    # image = cv2.GaussianBlur(image, (5, 5), 0)

    # Normalize pixel values
    image = image / 255.0

    # Inject noise
    noise = np.random.normal(0, 0.05, image.shape)
    image = image + noise
    image = np.clip(image, 0, 1)  # Ensure pixel values are still in [0, 1] range

    return image