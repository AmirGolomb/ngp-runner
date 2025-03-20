import os
import argparse


def rename_images(folder_path):
    # Ensure the provided path exists and is a directory
    if not os.path.isdir(folder_path):
        print(f"Error: The path '{folder_path}' is not a valid directory.")
        return

    # Iterate over files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file has a .png extension
        if filename.endswith(".png") and filename[:-4].isdigit():
            old_path = os.path.join(folder_path, filename)
            new_filename = f"{filename[:-4]}.jpg.png"
            new_path = os.path.join(folder_path, new_filename)

            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Rename PNG images to include .jpg in their filename.")
    # parser.add_argument("folder", help="Path to the folder containing images")
    # args = parser.parse_args()
    folder_path = r"images_masks"
    rename_images(folder_path)