import os
import shutil


def create_next_available_folder(base_path, scene_name):
    """
    Finds the smallest integer N such that "dji2-tN" does not exist in base_path,
    creates the folder, and copies the "images" folder from "dji2-t1" into it.

    :param base_path: The base directory where the folders exist.
    :param base_folder: The prefix of the folders to search (default: "dji2-t").
    :return: The path of the newly created folder.
    """

    # Start checking from dji2-t2 onwards
    n = 2
    while os.path.exists(os.path.join(base_path, f"{scene_name}-t{n}")):
        n += 1

    # Define new folder path
    new_folder_path = os.path.join(base_path, f"{scene_name}-t{n}")
    os.makedirs(new_folder_path)  # Create the new directory

    # Define source and destination image folder paths
    src_images_path = os.path.join(base_path, f"{scene_name}-t1", "images")
    dest_images_path = os.path.join(new_folder_path, "images")

    # Copy the "images" folder if it exists in "dji2-t1"
    if os.path.exists(src_images_path):
        shutil.copytree(src_images_path, dest_images_path)
    else:
        raise FileNotFoundError(f"Source images folder not found: {src_images_path}")

    return new_folder_path


# Example usage
base_path = r"C:\Users\amir\Documents\code\Instant-NGP-for-RTX-3000-and-4000\mydata"
scene_name = "dji2"
new_folder = create_next_available_folder(base_path, scene_name)
print(f"Created new folder: {new_folder}")
