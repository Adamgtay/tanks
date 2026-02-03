from PIL import Image
import os

def crop_and_save(image_path, output_folder, crop_size=64):
    # Open the image using Pillow
    img = Image.open(image_path)
    
    # Get the dimensions of the original image
    width, height = img.size
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Crop the image in 64-pixel increments
    for y in range(0, height, crop_size):
        for x in range(0, width, crop_size):
            # Define the bounding box for cropping
            box = (x, y, x + crop_size, y + crop_size)
            
            # Crop the image
            cropped_img = img.crop(box)
            
            # Generate the output file path
            output_path = os.path.join(output_folder, f"crop_{x}_{y}.png")
            
            # Save the cropped image as PNG
            cropped_img.save(output_path, "PNG")

# Example usage:
image_path = "/Users/Adam/Downloads/fire4_64.png"  # Replace with the path to your image
output_folder = "/Users/Adam/Desktop/pfe/tanks/tanks"  # Replace with the desired output folder

crop_and_save(image_path, output_folder)
