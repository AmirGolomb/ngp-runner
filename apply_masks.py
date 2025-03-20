import cv2
import os
import glob
import numpy as np

def apply_mask(image_path, mask_path, output_path):
    """
    Apply a black-white mask to an image.
    - Keeps original image where the mask is white (255).
    - Sets pixels to black where the mask is black (0).
    """
    # Load the original image and mask
    image = cv2.imread(image_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)  # Load as grayscale

    if image is None or mask is None:
        print(f"Skipping {image_path}, mask not found or unreadable.")
        return

    # Ensure the mask has the same dimensions as the image
    mask = cv2.resize(mask, (image.shape[1], image.shape[0]))

    # Convert mask to 3 channels to match the image
    mask_3ch = cv2.merge([mask, mask, mask])

    # Apply mask: where mask is 0 (black), set image to black; otherwise, keep original
    result = (image * (mask_3ch / 255)).astype(np.uint8)

    # Save the masked image
    cv2.imwrite(output_path, result)
    print(f"Saved masked image: {output_path}")

def process_folder(image_folder, mask_folder, output_folder):
    """
    Processes all images in the input folder by applying the corresponding masks.
    Assumes that images and masks have the same filenames.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_files = glob.glob(os.path.join(image_folder, "*.*"))

    for image_file in image_files:
        filename = os.path.basename(image_file)
        mask_file = os.path.join(mask_folder, filename) + ".png"

        if not os.path.exists(mask_file):
            print(f"Mask not found for {filename}. Skipping.")
            continue

        output_file = os.path.join(output_folder, filename)
        apply_mask(image_file, mask_file, output_file)

if __name__ == "__main__":
    # Set your folder paths
    image_folder = "images"
    mask_folder = "images_masks"
    output_folder = "images_masked"

    process_folder(image_folder, mask_folder, output_folder)
