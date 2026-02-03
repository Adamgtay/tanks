from PIL import Image
import os

def combine_with_single_image(input_folder, output_folder, single_image_path, crop_size=64):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of files in the input folder
    files_in_folder = os.listdir(input_folder)

    # Filter files to include only image files starting with "crop"
    image_files = [f for f in files_in_folder if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')) and f.startswith("crop")]

    # Open the single image
    single_image = Image.open(single_image_path)

    # Calculate the height of the new image (twice the height of the cropped instance)
    new_height = crop_size * 2

    for cropped_file in image_files:
        # Construct the full path for the cropped image
        cropped_path = os.path.join(input_folder, cropped_file)

        # Open the cropped image
        cropped_img = Image.open(cropped_path)

        # Calculate the scaling factor based on the width of the cropped image
        scaling_factor = cropped_img.width / single_image.width

        # Resize the single image proportionally
        single_image_resized = single_image.resize((int(single_image.width * scaling_factor), int(single_image.height * scaling_factor)))

        # Create a new image with the calculated dimensions
        combined_img = Image.new('RGBA', (cropped_img.width, new_height), (0, 0, 0, 0))

        # Paste the single image onto the top half of the new image
        combined_img.paste(single_image_resized, (0, 0), mask=single_image_resized)

        # Paste the cropped image centrally at the top of the new image
        combined_img.paste(cropped_img, (0, new_height // 2), mask=cropped_img)

        # Crop the combined image to remove empty space
        combined_img_cropped = crop_empty_space(combined_img)

        # Generate the output file path
        filename = os.path.splitext(cropped_file)[0]  # Use the original filename without extension
        output_path = os.path.join(output_folder, f"combined_{filename}.png")

        # Save the cropped combined image as PNG
        combined_img_cropped.save(output_path, "PNG")

def crop_empty_space(image):
    # Find bounding box of non-transparent pixels
    bbox = image.getbbox()

    # Crop the image to the bounding box
    cropped_image = image.crop(bbox)

    return cropped_image

# Example usage:
input_folder = "/Users/Adam/Desktop/pfe/tanks/tanks"
output_folder = "/Users/Adam/Desktop/pfe/tanks/tanks"
single_image_path = "/Users/Adam/Desktop/pfe/tanks/tanks/missile.png"

combine_with_single_image(input_folder, output_folder, single_image_path)
