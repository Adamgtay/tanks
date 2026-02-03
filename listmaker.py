import pygame, random

# Scale image and append to a target list (for single image)
def append_multiple_instances_of_scalable_image_to_list(num_of_images, scale,image):
    """
    

    Parameters:
    - target_list: The list to which scaled images will be appended.
    - num_of_images: The number of images to load and scale.
    - scale: The scale factor to be applied to each image.
    - file_pattern: The file pattern for the image files (e.g., "explosion{}.png").
    """
    target_list = []
    for i in range(1, num_of_images + 1):
        
        new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
        scaled_image = pygame.transform.scale(image, new_size)
        target_list.append(scaled_image)

    return target_list


# Scale images based on a file pattern and append them to a target list (for sequential images appended with number or letter)
def scale_images_and_format_append_to_new_list(num_of_images, scale, file_pattern):
    
    target_list = []
    for i in range(1, num_of_images + 1):
        image_path = file_pattern.format(i)
        original_image = pygame.image.load(image_path)
        new_size = (int(original_image.get_width() * scale), int(original_image.get_height() * scale))
        scaled_image = pygame.transform.scale(original_image, new_size)
        target_list.append(scaled_image)

    return target_list


# generate list of random integers
def gen_list_of_random_ints(min,max,num_of_ints):
    end_list = []
    for i in range(num_of_ints):
        end_list.append(random.randint(min,max))
    return end_list   

# simple appender
def append_lists(list_name,value):
                        list_name.append(value)


def generate_unique_coordinates(screen_width, screen_height, image_width, image_height, num_coordinates):
    x_coordinates = []
    y_coordinates = []

    while len(x_coordinates) < num_coordinates:
        x = random.randint(0, screen_width - image_width)
        y = random.randint(0, screen_height - image_height)

        # Check if the new coordinates overlap with existing ones
        """overlap = any(
            abs(x - existing_x) < image_width and abs(y - existing_y) < image_height
            for existing_x, existing_y in zip(x_coordinates, y_coordinates)
        )

        if not overlap:
            x_coordinates.append(x)
            y_coordinates.append(y)"""
        
        x_coordinates.append(x)
        y_coordinates.append(y)

    return x_coordinates, y_coordinates