import json
import subprocess
import time
import os

def run_command(command, description):
    """Run a system command and measure its execution time."""
    print(f"Starting: {description}")
    start_time = time.time()
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    end_time = time.time()
    elapsed_time = end_time - start_time
    if result.returncode == 0:
        print(f"Completed: {description} in {elapsed_time:.2f} seconds\n")
    else:
        print(f"Error during: {description}\n{result.stderr}")
    return elapsed_time

def fix_transforms_path(transforms_path):
    # Load JSON
    with open(transforms_path, "r") as f:
        data = json.load(f)
    # Fix file paths
    for frame in data["frames"]:
        frame["file_path"] = "./images/" + os.path.basename(frame["file_path"])
    # Save the updated JSON
    with open(transforms_path, "w") as f:
        json.dump(data, f, indent=4)
    print("Fixed file paths in transforms.json")


def main():
    # Paths (modify these according to your setup)
    run_folder = r"C:\Users\amir\Documents\code\Instant-NGP-for-RTX-3000-and-4000\mydata\dji2t4"
    colmap_executable = r"C:\Users\amir\Documents\code\colmap-x64-windows-cuda\COLMAP.bat"
    image_dir = os.path.join(run_folder, "images")
    database_path = os.path.join(run_folder, "database.db")
    sparse_dir = os.path.join(run_folder, "sparse")
    text_output_dir = os.path.join(run_folder, "sparse-text")
    colmap2nerf_script = r"C:\Users\amir\Documents\code\Instant-NGP-for-RTX-3000-and-4000\scripts\colmap2nerf.py"
    transforms_output = os.path.join(run_folder, "transforms.json")

    # Ensure output directories exist
    os.makedirs(sparse_dir, exist_ok=True)
    os.makedirs(text_output_dir, exist_ok=True)

    # Step 1: Feature Extraction
    feature_extraction_cmd = (
        f'"{colmap_executable}" feature_extractor --database_path "{database_path}" '
        f'--image_path "{image_dir}" --ImageReader.camera_model PINHOLE --ImageReader.single_camera 1'
    )
    feature_extraction_time = run_command(feature_extraction_cmd, "Feature Extraction")

    # Step 2: Feature Matching
    feature_matching_cmd = (
        f'"{colmap_executable}" exhaustive_matcher --database_path "{database_path}"'
    )
    feature_matching_time = run_command(feature_matching_cmd, "Feature Matching")

    # Step 3: Sparse Reconstruction
    sparse_reconstruction_cmd = (
        f'"{colmap_executable}" mapper --database_path "{database_path}" '
        f'--image_path "{image_dir}" --output_path "{sparse_dir}"'
    )
    sparse_reconstruction_time = run_command(sparse_reconstruction_cmd, "Sparse Reconstruction")

    # Step 4: Convert to Text Format
    model_converter_cmd = (
        f'"{colmap_executable}" model_converter --input_path "{sparse_dir}\\0" '
        f'--output_path "{text_output_dir}" --output_type TXT'
    )
    model_converter_time = run_command(model_converter_cmd, "Model Conversion to Text Format")

    # Step 5: Convert COLMAP Output to NeRF Format
    colmap2nerf_cmd = (
        f'python "{colmap2nerf_script}" --text "{text_output_dir}" --images "{image_dir}" '
        f'--out "{transforms_output}"'
    )

    colmap2nerf_time = run_command(colmap2nerf_cmd, "COLMAP to NeRF Conversion")
    fix_transforms_path(transforms_output)
    # Summary of execution times
    print("Execution Time Summary:")
    print(f"Feature Extraction: {feature_extraction_time:.2f} seconds")
    print(f"Feature Matching: {feature_matching_time:.2f} seconds")
    print(f"Sparse Reconstruction: {sparse_reconstruction_time:.2f} seconds")
    print(f"Model Conversion to Text Format: {model_converter_time:.2f} seconds")
    print(f"COLMAP to NeRF Conversion: {colmap2nerf_time:.2f} seconds")

if __name__ == "__main__":
    main()
