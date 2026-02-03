import pygame

def rotate_image(name_of_image,angle):
    rotated_image = pygame.transform.rotate(name_of_image, angle)
    return rotated_image

def update_object_position(objectX, objectY,object_height,object_width, new_xpos, new_ypos, screen_width, screen_height):
    # Update Y position
    objectY += new_ypos
    if objectY <= 0:
        objectY = 0
    if objectY >= screen_height - object_height:
        objectY = screen_height - object_height

    # Update X position
    objectX += new_xpos
    if objectX <= 0:
        objectX = 0
    if objectX >= screen_width - object_width:
        objectX = screen_width - object_width

    return objectX, objectY 