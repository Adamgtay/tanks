import os, pygame

# Function to load images from a directory: could make more dynamic to allow sounds into sound_dict
def load_images_from_directory(directory):
    image_dict = {}
    for filename in os.listdir(directory):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(directory, filename)
            image = pygame.image.load(image_path)
            # Remove the file extension to use as the key
            key = os.path.splitext(filename)[0]
            image_dict[key] = image
    return image_dict


# make a function to blit any image
def show_image(x, y, images, screen):
    
    screen.blit(images, (x, y))

# make a function to blit any image
def show_image_centre_snap(x, y, images, screen):

     # Get the width and height of the text surface
    text_width, text_height = images.get_size()
    
    screen.blit(images, (x-(text_width/2), y-(text_height/2)))

# measuring number of images to number of frames to produce animation sequence
def disperse_images_across_frames(x, y, list_of_events, image_sequence_list,num_of_frames,screen):
    for i in range(len(list_of_events)):
        if list_of_events[i] <= num_of_frames:  # Length of explosion in frames
            image_index = list_of_events[i] // (num_of_frames // len(image_sequence_list)) # // is int division
            if 0 <= image_index < len(image_sequence_list):
                show_image(x[i], y[i],image_sequence_list[image_index],screen)
            list_of_events[i] += 1
           
         


# Function to display text with a specified font
def display_text(screen,text, x, y, size=36, font_path=None, color=(255, 255, 255)):
    # Create a pygame font object
    font = pygame.font.Font(font_path, size)

    # Render the text
    text_surface = font.render(text, True, color)

    

    #print(text_width,text_height)
    
    # Blit the text surface onto the screen
    show_image(x, y,text_surface,screen)

    

