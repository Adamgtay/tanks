from pygame import mixer
import pygame,imageloader, ints, listmaker,collisions,random

# make function for basic setup
def basic_game_setup(screen_w,screen_h,game_title,game_length_millisec):
    pygame.init()
    clock = pygame.time.Clock()

    # game duration
    GAME_DURATION = game_length_millisec
    # Initialize the start time
    start_time = pygame.time.get_ticks()

    # screen dimensions
    screen_w=800
    screen_h=600


    # create screen
    screen = pygame.display.set_mode((screen_w,screen_h))

    # title
    pygame.display.set_caption(game_title)

    return clock,GAME_DURATION,start_time,screen_w,screen_h,screen

def fire_weapon(sound_fx,weapon_image,x_start,y_start,screen):
    # weapon sound fx
    weapon_sound = mixer.Sound(sound_fx)
    weapon_sound.play()
    # blit weapon at current position
    imageloader.show_image(x_start,y_start,weapon_image,screen)


def initiate_weapon(weapon_count,player_x_pos,player_y_pos,weapon_sound,weapon_image,screen_set_mode,weapon_x_list,weapon_y_list,weapon_instances_list,weapon_speed):
    # if ammo is present, fire weapon
    if weapon_count > 0:
                    # position for missile to start trajectory
                    startX = ints.integer_adjuster(int(player_x_pos),16) # int to make whole number
                    startY = ints.integer_adjuster(int(player_y_pos),0) 

                    # plays weapon sound and blits weapon image at start point
                    fire_weapon(weapon_sound,weapon_image,startX,startY,screen_set_mode)
                    
                    # update missile data lists
                    
                    listmaker.append_lists(weapon_y_list,startY) 
                    listmaker.append_lists(weapon_x_list,startX)
                    listmaker.append_lists(weapon_instances_list,weapon_speed)
                    
                    
                    weapon_count -= 1
    return weapon_count


def update_weapon_position(weapon_x_list,weapon_y_list,weapon_speed_list,weapon_image,screen_set_mode):
        if len(weapon_y_list) > 0:
            for i in list(range(len(weapon_x_list))):
                weapon_y_list[i] += weapon_speed_list[i]
                
                     
                     
                
                     
                imageloader.show_image(weapon_x_list[i], weapon_y_list[i],weapon_image,screen_set_mode)
            

def check_for_weapon_collision(weapon_x_list,weapon_y_list,weapon_speed_list,target_x_list,target_y_list,target_image_list,collision_tolerance,num_of_collisions,impact_list,impact_x_list,impact_y_list,impact_sound,collide_x_adjust,collide_y_adjust):
        i = 0
        while i < len(weapon_y_list):
            j = 0
            while j < len(target_x_list):
                collision = collisions.isCollision(target_x_list[j], target_y_list[j], weapon_x_list[i], weapon_y_list[i], collision_tolerance,16)
                if collision:
                        num_of_collisions += 1

                        # append collision info to explosion lists

                        impact_list.append(0)
                        impact_x_list.append(target_x_list[j]+collide_x_adjust)
                        impact_y_list.append(target_y_list[j]+collide_y_adjust)

                        # explosion sound
                        collide_sound = mixer.Sound(impact_sound)
                        collide_sound.play()

                        
                        

                        
                        # remove missile instance
                        del weapon_x_list[i]
                        del weapon_y_list[i]
                        del weapon_speed_list[i]

                        # remove collision target
                        del target_x_list[j]
                        del target_y_list[j]
                        del target_image_list[j]
                        i -= 1  # Adjust index since we removed an element
                        break  # Exit inner loop after collision

                j += 1

            i += 1

        return num_of_collisions            

def check_for_player_missile_collision(weapon_x_list,weapon_y_list,player_x,player_y,collision_tolerance,impact_list,impact_x_list,impact_y_list,impact_sound,collide_x_adjust,collide_y_adjust):
        i = 0
        while i < len(weapon_y_list):
                
                collision = collisions.isCollision(player_x, player_y, weapon_x_list[i], weapon_y_list[i], collision_tolerance,16)
                if collision:
                        

                        # append collision info to explosion lists

                        impact_list.append(0)
                        impact_x_list.append(player_x+collide_x_adjust)
                        impact_y_list.append(player_y+collide_y_adjust)

                        # explosion sound
                        collide_sound = mixer.Sound(impact_sound)
                        collide_sound.play()
                        return True
                i += 1
        return False        

        

def check_for_ammo_collision(player_x, player_y, target_x_list, target_y_list, collision_tolerance, current_missile_count):
    j = 0
    new_missile_count = current_missile_count  # Initialize outside the loop

    while j < len(target_x_list):
        collision = collisions.isCollision(target_x_list[j], target_y_list[j], player_x, player_y, collision_tolerance, 0)
        if collision:
            num_of_missiles_collected = random.randint(50, 100)
            new_missile_count += num_of_missiles_collected

            # remove collision target
            del target_x_list[j]
            del target_y_list[j]

            break  # Exit inner loop after collision

        j += 1

    return new_missile_count    

def check_for_tank_collision(player_x, player_y, target_x_list,target_y_list,target_image_list,collision_tolerance,num_of_collisions,impact_list,impact_x_list,impact_y_list,impact_sound,collide_x_adjust,collide_y_adjust):
    j = 0
      # Initialize outside the loop

    while j < len(target_x_list):
        collision = collisions.isCollision(target_x_list[j], target_y_list[j], player_x, player_y, collision_tolerance, 0)
        if collision:
            num_of_collisions += 1

                        # append collision info to explosion lists

            impact_list.append(0)
            impact_x_list.append(target_x_list[j]+collide_x_adjust)
            impact_y_list.append(target_y_list[j]+collide_y_adjust)

            impact_list.append(0)
            impact_x_list.append(player_x+collide_x_adjust)
            impact_y_list.append(player_y+collide_y_adjust)

                        # explosion sound
            collide_sound = mixer.Sound(impact_sound)
            collide_sound.play()
            

            del target_x_list[j]
            del target_y_list[j]
            del target_image_list[j]

            return True        

        j += 1

def check_for_tank_screen_exit(impact_list,impact_x_list,impact_y_list,player_x,player_y,screen_y, target_x_list,target_y_list,target_image_list,image_height,collide_x_adjust,collide_y_adjust,impact_sound):
    j = 0
      # Initialize outside the loop

    while j < len(target_x_list):
        #collision = collisions.isCollision(target_x_list[j], target_y_list[j], screen_x, screen_y, collision_tolerance, 0)
        if target_y_list[j] >= screen_y-(image_height/2):
            #num_of_collisions += 1

            # append collision info to explosion lists

            impact_list.append(0)
            impact_x_list.append(target_x_list[j]+collide_x_adjust)
            impact_y_list.append(target_y_list[j]+collide_y_adjust)

            impact_list.append(0)
            impact_x_list.append(player_x+collide_x_adjust)
            impact_y_list.append(player_y+collide_y_adjust)

                        # explosion sound
            collide_sound = mixer.Sound(impact_sound)
            collide_sound.play()
            

            del target_x_list[j]
            del target_y_list[j]
            del target_image_list[j]

            return True
                    

        j += 1

def check_for_enemy_missile_fire(enemy_missile_count_list,enemy_missile_x_list,enemy_missile_y_list,enemy_missile_instances_list,enemy_missile_speed,player_x,player_y,target_x_list,screen,weapon_image,enemy_x_pos_list,enemy_y_pos_list):
    j = 0
      # Initialize outside the loop

    while j < len(target_x_list):
        #collision = collisions.isCollision(target_x_list[j], target_y_list[j], screen_x, screen_y, collision_tolerance, 0)
        if target_x_list[j] == player_x:
             #print("targeted!")
             enemy_missile_count_list[j] = initiate_weapon(enemy_missile_count_list[j],enemy_x_pos_list[j],enemy_y_pos_list[j],"launch.wav",weapon_image,screen,enemy_missile_x_list,enemy_missile_y_list,enemy_missile_instances_list,enemy_missile_speed)
             #print(enemy_missile_count_list[j])
            
                    

        j += 1
    

# blit enemy pos: make this into function and use for ammo crates also
def enemy_movement(min_left_pos,max_right_pos,image_list,x_list,y_list,speed_list,screen_set_mode,image_width,image_height,left_speed,right_speed,down_speed):
        for i in range(len(image_list)):
            
            imageloader.show_image(x_list[i],y_list[i],image_list[i],screen_set_mode)
            x_list[i] += speed_list[i] # enemy by default moves to right
            if x_list[i] >= max_right_pos:
                #print("length: ", len(image_list))
                x_list[i] = max_right_pos
                #print("position: ", x_list[i])
                speed_list[i] = left_speed # change speed of tank to -2 to move left
                #print("speed: ",speed_list[i])
                y_list[i] += image_height # tank moves down
                
                
                
            elif x_list[i] <= min_left_pos:
                x_list[i] = min_left_pos
                speed_list[i] = right_speed  # change spped to move left
                y_list[i] += image_height # tank moves down
                 
                
                


# blit enemy pos: make this into function and use for ammo crates also
def update_ammo_crate_position(weapon_x_list,weapon_y_list,weapon_speed_list,weapon_count,weapon_image,screen_height,crate_height,screen_set_mode):
        if weapon_count > 0:
            for i in list(range(len(weapon_x_list))):
                weapon_y_list[i] += weapon_speed_list[i]
                if weapon_y_list[i] >= (screen_height-crate_height)-5:
                      weapon_y_list[i] = (screen_height-crate_height)-5
    
                imageloader.show_image(weapon_x_list[i], weapon_y_list[i],weapon_image,screen_set_mode)
                 

# Update the time since the last ammo crate release - make function for any ammo crate
def release_ammo_crate(crate_speed,interval_increment,time_since_last_ammo,ammo_crate_count,ammo_x_list,ammo_y_list,ammo_speed_list,ammo_interval,min_x,max_x,ammo_width):

        time_since_last_ammo += interval_increment
        #print(time_since_last_ammo_crate)

        # Check if it's time to release an ammo crate
        if time_since_last_ammo >= ammo_interval:
            
            ammo_crate_count += 1
            ammo_x_list.append(random.randint(min_x,max_x-ammo_width))
            ammo_y_list.append(1)
            ammo_speed_list.append(crate_speed)
            # Reset the timer
            time_since_last_ammo = 0

        return ammo_crate_count,time_since_last_ammo    



# graphics data
def game_element_start(start_x,start_y,element_h,element_w,speed_x,speed_y):
    return start_x,start_y,element_h,element_w,speed_x,speed_y 


def premade_lists_of_units(num_of_units,scale_image,unit_image,unit_speed_lo,unit_speed_hi,max_x,max_y,unit_w,unit_h,num_of_missiles_per_tank):

    units = listmaker.append_multiple_instances_of_scalable_image_to_list(num_of_units,scale_image,unit_image)
    # enemy coordinates and speed lists
    
    unitX_list,unitY_list = listmaker.generate_unique_coordinates(max_x,max_y,unit_w,unit_h,len(units))
    unit_speed_list = listmaker.gen_list_of_random_ints(unit_speed_lo,unit_speed_hi,len(units))

    blue_tank_missile_count_list = []
    i = 0
    while i< num_of_units:
         blue_tank_missile_count_list.append(num_of_missiles_per_tank)
         i += 1
         
         
    

    return units,unitX_list,unitY_list,unit_speed_list,unit_w,unit_h,blue_tank_missile_count_list


def ammo_lists(weapon_speed,weapon_supply):
    fireY_list = []
    fireX_list =[] 
    current_weapon_instances = []
    
    return fireX_list,fireY_list,current_weapon_instances,weapon_speed,weapon_supply





# Initialize variables for ammo crate
def ammo_crate(crate_speed,interval,increment,start_time,start_count):

    crateX_list = []
    crateY_list = []
    crate_speed_list = []
    
    return crate_speed, interval, increment,start_time, start_count,crateX_list,crateY_list,crate_speed_list


# make up empty lists and image sequence list for animations
def empty_lists_for_animation(num_of_images,image_scale,file_pattern):
    instance_list =[]
    animation_location_x_list = []
    animation_location_y_list = []
    # image lists for animations
    # scale  images and append to a list
    list_of_images = listmaker.scale_images_and_format_append_to_new_list(num_of_images, image_scale, file_pattern)

    return instance_list,animation_location_x_list,animation_location_y_list,list_of_images


# add enemy units
def add_units(num_of_units,scale_image,unit_image,max_x,max_y,unit_w,unit_h,unit_speed_lo,unit_speed_hi,existing_unit_image_list,existing_unit_x_list,existing_unit_y_list,existing_unit_speed_list,existing_unit_missile_count_list,missiles_per_unit):

        # make new list of unit images to add
        new_units_image_list = listmaker.append_multiple_instances_of_scalable_image_to_list(num_of_units,scale_image,unit_image)
        
        # new units coordinates and speed lists
        new_unitX_list,new_unitY_list = listmaker.generate_unique_coordinates(max_x,max_y,unit_w,unit_h,len(new_units_image_list))
        new_unit_speed_list = listmaker.gen_list_of_random_ints(unit_speed_lo,unit_speed_hi,len(new_units_image_list))

        i=0
        new_units_missile_count_list = []
        while i < num_of_units:
             new_units_missile_count_list.append(missiles_per_unit)
             i += 1
             
        # join new lists to existing lists
        #print(new_unitX_list)
        #print(new_units_image_list)
        existing_unit_image_list += new_units_image_list
        existing_unit_x_list += new_unitX_list
        existing_unit_y_list += new_unitY_list
        existing_unit_speed_list += new_unit_speed_list
        existing_unit_missile_count_list += new_units_missile_count_list


       