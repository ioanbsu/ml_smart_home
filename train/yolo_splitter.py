# example execution
# python yolo_splitter.py --source=/Users/ioanbsu/Downloads/HomeAutomationTrainingDataset --destination /Users/ioanbsu/Downloads/HomeAutomationTrainingDatasetSplit --train_ratio=0.6 --test_ratio=0.0 --val_ratio=0.4
import argparse
import os
import random
import shutil

import yaml


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, help='path for the source of the yolo dataset')
    parser.add_argument('--destination', type=str, help='output path for where to put generated slit dataset to')
    parser.add_argument('--train_ratio', type=float, default=0.8, help='Ratio of train images')
    parser.add_argument('--test_ratio', type=float, default=0.1, help='Ratio of test images')
    parser.add_argument('--val_ratio', type=float, default=0.1, help='Ratio of validate images')
    parser.add_argument('--cleanup_output_dir', type=bool, default=True,
                        help='Defined whether to cleanup output directory before uploading all datasets into it or not.')
    opt = parser.parse_args()
    return opt


args = parse_opt()

# Set the desired split ratios
train_ratio = args.train_ratio
test_ratio = args.test_ratio
val_ratio = args.val_ratio
if (test_ratio + train_ratio + val_ratio) != 1:
    raise Exception(
        "Provided incompatible ratios for test, validate and train folders. The sum of ration has to b1 equal to 1")

# Set the path to your original COCO dataset
dataset_source_path = args.source
# Set the path to store the train, test, and validation subsets
destination_split_folder = args.destination
train_path = '%s/train' % destination_split_folder
test_path = '%s/test' % destination_split_folder
val_path = '%s/val' % destination_split_folder
# Whether to cleanup output directory or not
delete_output_dir = args.cleanup_output_dir
if delete_output_dir and os.path.exists(destination_split_folder):
    shutil.rmtree(destination_split_folder)

# Create the output directories
images_folder = 'images'
labels_folder = 'labels'
os.makedirs(os.path.join(train_path, images_folder), exist_ok=True)
os.makedirs(os.path.join(train_path, labels_folder), exist_ok=True)
os.makedirs(os.path.join(test_path, images_folder), exist_ok=True)
os.makedirs(os.path.join(test_path, labels_folder), exist_ok=True)
os.makedirs(os.path.join(val_path, images_folder), exist_ok=True)
os.makedirs(os.path.join(val_path, labels_folder), exist_ok=True)

# Get the list of image files in the dataset
image_files = [file for file in os.listdir(os.path.join(dataset_source_path, images_folder)) if file.endswith('.jpg')]

# Shuffle the list of image files
# random.seed(42)  # Set a random seed for reproducibility
random.shuffle(image_files)

# Calculate the number of images for each subset based on the ratios
num_images = len(image_files)
num_train = int(num_images * train_ratio)
num_test = int(num_images * test_ratio)
num_val = num_images - num_train - num_test

# Split the image files into train, test, and validation subsets
train_files = image_files[:num_train]
test_files = image_files[num_train:num_train + num_test]
val_files = image_files[num_train + num_test:]


# Function to copy files from source to destination
def copy_files(source_dir, destination_dir, filenames):
    for filename in filenames:
        img_source = os.path.join(dataset_source_path, images_folder, filename)
        img_destination = os.path.join(destination_dir, images_folder, filename)
        shutil.copy(img_source, img_destination)

        label_source = os.path.join(dataset_source_path, 'labels', filename.replace('.jpg', '.txt'))
        label_destination = os.path.join(destination_dir, 'labels', filename.replace('.jpg', '.txt'))
        shutil.copy(label_source, label_destination)


# Copy files to the train folder
copy_files(dataset_source_path, train_path, train_files)

# Copy files to the test folder
copy_files(dataset_source_path, test_path, test_files)

# Copy files to the validation folder
copy_files(dataset_source_path, val_path, val_files)

classes_file = os.path.join(dataset_source_path + '/classes.txt')
with open(classes_file, 'r') as file:
    class_values = file.readlines()
class_values = [clazz.strip() for clazz in class_values]
classes = len(class_values)
data = {
    'train': '../train/images',
    'val': '../val/images',
    'test': '../test/images',
    'nc': classes,
    'names': class_values
}

data_file_name = os.path.join(destination_split_folder + '/data.yaml')
with open(data_file_name, 'w') as file:
    yaml.dump(data, file)
