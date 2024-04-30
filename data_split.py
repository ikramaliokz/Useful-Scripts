import os
import shutil

dataset_dir = '/home/athenaai/Desktop/Lego/RealImagesTest/photos'
train_dir = 'train'
val_dir = 'val'
test_dir = 'test'

# Create training, validation, and test directories
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Specify the percentage for validation and test data
validation_split = 0.2
test_split = 0.1

for class_folder in os.listdir(dataset_dir):
    class_path = os.path.join(dataset_dir, class_folder)
    train_class_path = os.path.join(train_dir, class_folder)
    val_class_path = os.path.join(val_dir, class_folder)
    test_class_path = os.path.join(test_dir, class_folder)

    os.makedirs(train_class_path, exist_ok=True)
    os.makedirs(val_class_path, exist_ok=True)
    os.makedirs(test_class_path, exist_ok=True)

    # List all the image files in the class folder
    images = os.listdir(class_path)

    # Calculate the number of images for validation and test sets
    num_validation = int(validation_split * len(images))
    num_test = int(test_split * len(images))

    # if you want to just copy the files you may use copy instead of move
    # Move images to the validation directory 
    for img in images[:num_validation]:
        src = os.path.join(class_path, img)
        dest = os.path.join(val_class_path, img)
        shutil.move(src, dest)

    # Move images to the test directory
    for img in images[num_validation:num_validation + num_test]:
        src = os.path.join(class_path, img)
        dest = os.path.join(test_class_path, img)
        shutil.move(src, dest)

    # Move the remaining images to the training directory
    for img in images[num_validation + num_test:]:
        src = os.path.join(class_path, img)
        dest = os.path.join(train_class_path, img)
        shutil.move(src, dest)