import cv2
import os
import glob
import numpy as np


def create_mask_from_roi(image, roi):
    """
    Create a binary mask with white (255) in the ROI and black (0) elsewhere.
    """
    # Create an empty mask with the same dimensions as the image (single channel)
    mask = np.zeros(image.shape[:2], dtype="uint8")
    x, y, w, h = roi
    mask[y:y + h, x:x + w] = 255  # white inside the selected rectangle
    return mask


def main(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List image files (you can adjust the glob pattern for specific extensions)
    image_files = glob.glob(os.path.join(input_folder, "*.*"))

    for image_file in image_files:
        image = cv2.imread(image_file)
        if image is None:
            print(f"Failed to load {image_file}. Skipping.")
            continue

        # Display the image and allow the user to select an ROI.
        # Instructions: Draw a rectangle around the window and press ENTER or SPACE. Press 'c' to cancel.
        # roi = cv2.selectROI("Select ROI (press ENTER/SPACE to confirm, c to cancel)", image, fromCenter=False,
        #                     showCrosshair=True)
        window_name = "Select ROI (press ENTER/SPACE to confirm, c to cancel)"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 2000, 800)  # Set desired width and height
        roi = cv2.selectROI(window_name, image, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow(window_name)
        # cv2.destroyWindow("Select ROI (press ENTER/SPACE to confirm, c to cancel)")

        # roi returns (x, y, width, height). If no ROI is selected, width and height will be 0.
        if roi[2] > 0 and roi[3] > 0:
            mask = create_mask_from_roi(image, roi)
            # Construct a filename for the mask. For instance, if image is "012.jpg", mask becomes "012.png"
            base = os.path.basename(image_file)
            mask_filename = os.path.splitext(base)[0] + ".jpg.png"
            mask_filepath = os.path.join(output_folder, mask_filename)
            cv2.imwrite(mask_filepath, mask)
            print(f"Saved mask: {mask_filepath}")
        else:
            print(f"No ROI selected for {image_file}. Skipping.")


if __name__ == "__main__":
    # Change these paths to the directories containing your images and where you want to save masks.
    input_folder = "images"
    output_folder = input_folder + "_masks"
    main(input_folder, output_folder)
