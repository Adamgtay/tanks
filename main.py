import pygame
import imageloader
import alter_image
import listmaker
import tanks_elements
import soundloader
import random
from pygame import mixer


# basic setup
CLOCK, GAME_DURATION, START_TIME, SCREEN_WIDTH, SCREEN_HEIGHT, screen = tanks_elements.basic_game_setup(
    800, 600, "Tank Commander", 60000)

# frames per second
FPS = 60


FONT_LOCATION = "/Users/Adam/Desktop/coding/pfe/tanks/tanks/dogica.ttf"

# image dictionary
IMAGE_DICT = imageloader.load_images_from_directory(
    "/Users/Adam/Desktop/coding/pfe/tanks/tanks/images")

# app icon
pygame.display.set_icon(IMAGE_DICT['explode'])

running = True


def level_one(running):
    # starting location for player tank
    player_X, player_Y, player_height, player_width, current_player_x_speed, current_player_y_speed = tanks_elements.game_element_start(
        (SCREEN_WIDTH/2)-32, (SCREEN_HEIGHT/3)+400, 64, 64, 0, 0)

    # blue_tank tank image rotate
    blue_tank = alter_image.rotate_image(IMAGE_DICT["tank_blue"], 180)
    # premake lists for different batches of tanks. append lists names with a,b,c,d etc. for i in [a,b,c,d...]
    blue_tank_image_list, blue_tank_X_coor_list, blue_tank_Y_coor_list, blue_tank_speed_list, blue_tank_width, blue_tank_height, enemy_missile_count_list = tanks_elements.premade_lists_of_units(
        6, 1, blue_tank, 2, 2, SCREEN_WIDTH, SCREEN_HEIGHT-500, 64, 64, 6)

    # missiles (empty lists to be populated when weapon is fired)
    missile_x_coor_list, missile_y_coor_list, missile_instances_list, missile_speed, missile_count = tanks_elements.ammo_lists(
        -15, 100)

    # blue_tank missile lists
    enemy_missile_x_list, enemy_missile_y_list, enemy_missile_instances_list, enemy_missile_speed, enemy_missile_count = tanks_elements.ammo_lists(
        10, 6)

    # empty missile ammo crate lists
    missile_crate_v, missile_crate_interval, crate_increment, time_since_last_missile_crate, missile_crate_count, missile_crateX_list, missile_crateY_list, missile_crate_speed_list = tanks_elements.ammo_crate(
        1, random.randint(3000, 5000), 10, 0, 0)

    # empty lists for explosion data
    explosion_instance_list, explosions_x_list, explosions_y_list, explosion_image_list = tanks_elements.empty_lists_for_animation(
        16, 0.25, "images/explosion{}.png")

    # number of collisions from missiles
    collision_count = 0
    collide_x_adjust = -16
    collide_y_adjust = -10

    # player mortality
    player_alive = True
    player_collision = False
    player_win = False
    # Number of seconds to wait after a tank collision (for explosion animation to run)
    delay_after_player_death = 2
    frames_since_player_death = 0  # Counter to keep track of frames since collision
    frames_since_player_win = 0
    delay_after_player_win = 2

    # gme end
    end_title_frame_count = 0
    end_title_seconds = 5

    # respawn data
    blue_tanks_spawned = False
    enemy_tank_exit = False
    respawn_interval = 5000
    spawn_unit_speed = 5
    num_spawned = 4

    # background sound - continuous
    soundloader.main_music_load("DT_theme - 01.06.2024, 21.58.mp3", -1)

    # game loop
    while running:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - START_TIME

        imageloader.show_image(0, 0, IMAGE_DICT['mud'], screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_player_y_speed -= 3
                if event.key == pygame.K_DOWN:
                    current_player_y_speed += 3
                if event.key == pygame.K_RIGHT:
                    # rotate_image(main_tank,-90, player_X,player_Y)
                    current_player_x_speed += 3
                if event.key == pygame.K_LEFT:
                    # rotate_image(main_tank,90, player_X,player_Y)
                    current_player_x_speed -= 3
                if event.key == pygame.K_SPACE:
                    # missile initiation and adjust missile supply
                    missile_count = tanks_elements.initiate_weapon(
                        missile_count, player_X, player_Y, "launch.wav", IMAGE_DICT["missile"], screen, missile_x_coor_list, missile_y_coor_list, missile_instances_list, missile_speed)

            # if directional keys are released, then tank does not move
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    current_player_y_speed = 0
                    current_player_x_speed = 0

        # this block of logic only executes if player_alive is true and no game over conditions have been met.
        if player_alive:

            # blue_tank missile initiate - this works. it is finding the player to target.
            tanks_elements.check_for_enemy_missile_fire(enemy_missile_count_list, enemy_missile_x_list, enemy_missile_y_list, enemy_missile_instances_list,
                                                        enemy_missile_speed, player_X, player_Y, blue_tank_X_coor_list, screen, IMAGE_DICT["enemy_missile"], blue_tank_X_coor_list, blue_tank_Y_coor_list)

            # based on time interval, an ammo crate will be released. this is for a missile crate. updates ammo crate lists and resets time interval to zero.
            missile_crate_count, time_since_last_missile_crate = tanks_elements.release_ammo_crate(
                missile_crate_v, crate_increment, time_since_last_missile_crate, missile_crate_count, missile_crateX_list, missile_crateY_list, missile_crate_speed_list, missile_crate_interval, 0, SCREEN_WIDTH, 32)

            # if the ammo crate time interval has been reached, this will update the position of ammo crate, including resting in final position.
            tanks_elements.update_ammo_crate_position(
                missile_crateX_list, missile_crateY_list, missile_crate_speed_list, missile_crate_count, IMAGE_DICT["crate"], SCREEN_HEIGHT, 32, screen)

            # revise tank x and y coordinates depending on key pressed
            player_X, player_Y = alter_image.update_object_position(
                player_X, player_Y, player_width, player_height, current_player_x_speed, current_player_y_speed, SCREEN_WIDTH, SCREEN_HEIGHT)

            # if missiles have been launched, this updates missile position
            tanks_elements.update_weapon_position(
                missile_x_coor_list, missile_y_coor_list, missile_instances_list, IMAGE_DICT["missile"], screen)

            # if enemy missiles have been launched, this updates missile position
            tanks_elements.update_weapon_position(
                enemy_missile_x_list, enemy_missile_y_list, enemy_missile_instances_list, IMAGE_DICT["enemy_missile"], screen)

            #  this updates both missile and blue_tank lists depending if collsion has occured
            collision_count = tanks_elements.check_for_weapon_collision(missile_x_coor_list, missile_y_coor_list, missile_instances_list, blue_tank_X_coor_list, blue_tank_Y_coor_list,
                                                                        blue_tank_image_list, 25, collision_count, explosion_instance_list, explosions_x_list, explosions_y_list, "explode.wav", collide_x_adjust, collide_y_adjust)

            #  returns true if player is hot by enemy missile, therefore triggering game over. returns false otherwise

            player_collision = tanks_elements.check_for_player_missile_collision(
                enemy_missile_x_list, enemy_missile_y_list, player_X, player_Y, 27, explosion_instance_list, explosions_x_list, explosions_y_list, "explode.wav", collide_x_adjust, collide_y_adjust)

            # checks for player tank colliding with blue_tank tank. atm the blue_tank just explodes.
            tank_collision = tanks_elements.check_for_tank_collision(player_X, player_Y, blue_tank_X_coor_list, blue_tank_Y_coor_list, blue_tank_image_list,
                                                                     27, collision_count, explosion_instance_list, explosions_x_list, explosions_y_list, "explode.wav", collide_x_adjust, collide_y_adjust)

            #  this checks if player has picked up ammo crate and increases weapon supply
            missile_count = tanks_elements.check_for_ammo_collision(
                player_X, player_Y, missile_crateX_list, missile_crateY_list, 30, missile_count)

            # check enenmy screen bottom exit
            enemy_tank_exit = tanks_elements.check_for_tank_screen_exit(explosion_instance_list, explosions_x_list, explosions_y_list, player_X,
                                                                        player_Y, SCREEN_HEIGHT, blue_tank_X_coor_list, blue_tank_Y_coor_list, blue_tank_image_list, blue_tank_height, -26, -10, "explode.wav")
            # print(enemy_tank_exit)

            # spawn new tanks
            if not blue_tanks_spawned:
                if elapsed_time >= respawn_interval:
                    # Update the positions of blue tanks
                    tanks_elements.add_units(num_spawned, 1, blue_tank, SCREEN_WIDTH-blue_tank_width, 200, blue_tank_width, blue_tank_height, spawn_unit_speed,
                                             spawn_unit_speed, blue_tank_image_list, blue_tank_X_coor_list, blue_tank_Y_coor_list, blue_tank_speed_list, enemy_missile_count_list, 6)
                    respawn_interval += 5000
                    # spawn_unit_speed += 1
                    num_spawned += 2
                    blue_tanks_spawned = True

            if blue_tanks_spawned:
                if elapsed_time >= respawn_interval:
                    # Update the positions of blue tanks
                    tanks_elements.add_units(num_spawned, 1, blue_tank, SCREEN_WIDTH-blue_tank_width, 200, blue_tank_width, blue_tank_height, spawn_unit_speed,
                                             spawn_unit_speed, blue_tank_image_list, blue_tank_X_coor_list, blue_tank_Y_coor_list, blue_tank_speed_list, enemy_missile_count_list, 6)
                    respawn_interval += 5000
                    # spawn_unit_speed += 1
                    num_spawned += 2
                    blue_tanks_spawned = False

            # blit player tank posotion
            imageloader.show_image(
                player_X, player_Y, IMAGE_DICT["tank"], screen)
        else:
            frames_since_player_death += 1
            frames_since_player_win += 1

        # blit blue_tank tank positions
        if not player_win:
            tanks_elements.enemy_movement(0, SCREEN_WIDTH-blue_tank_width, blue_tank_image_list, blue_tank_X_coor_list,
                                          blue_tank_Y_coor_list, blue_tank_speed_list, screen, blue_tank_width, blue_tank_height, -2, 2, blue_tank_height+15)
        if player_win:
            # revise tank x and y coordinates depending on key pressed
            player_X, player_Y = alter_image.update_object_position(
                player_X, player_Y, player_width, player_height, current_player_x_speed, current_player_y_speed, SCREEN_WIDTH, SCREEN_HEIGHT)
            # blit player tank posotion
            imageloader.show_image(
                player_X, player_Y, IMAGE_DICT["tank"], screen)
        # if there are collsions, this will play missile explosions.
        imageloader.disperse_images_across_frames(
            explosions_x_list, explosions_y_list, explosion_instance_list, explosion_image_list, 60, screen)

        # displays player score and number of missiles remaining
        imageloader.display_text(
            screen, f"Score: {collision_count}", 10, 10, 16, font_path=FONT_LOCATION, color=(255, 255, 255))
        imageloader.display_text(
            screen, f"Missiles: {missile_count}", 10, 40, 16, font_path=FONT_LOCATION, color=(255, 255, 255))

        # Calculate remaining time
        remaining_time = max(0, GAME_DURATION - elapsed_time)
        # print(remaining_time)

        # Display remaining time on the screen
        imageloader.display_text(
            screen, f"Time: {remaining_time // 1000} seconds", 10, 70, 16, font_path=FONT_LOCATION, color=(255, 255, 255))

        # game over conditions that trigger player_alive to false, initiating game over sequence.
        if player_alive:
            if tank_collision or player_collision or (elapsed_time >= GAME_DURATION):
                player_alive = False
                frames_since_player_death = 0
            elif collision_count >= 50:
                player_alive = False
                player_win = True
                frames_since_player_win = 0

        # checking  game over conditions to display game over. there is a delay to allow last explosion to finsih before 'game over' txt appears.
        if not player_alive and not player_win:
            if frames_since_player_death/FPS > delay_after_player_death:

                if elapsed_time >= GAME_DURATION:
                    imageloader.show_image_centre_snap(
                        SCREEN_WIDTH/2, (SCREEN_HEIGHT/2)-40, IMAGE_DICT["TIME_UP"], screen)
                elif tank_collision or player_collision:
                    imageloader.show_image_centre_snap(
                        SCREEN_WIDTH/2, (SCREEN_HEIGHT/2)-40, IMAGE_DICT["ka_boom"], screen)

                imageloader.show_image_centre_snap(
                    SCREEN_WIDTH/2, SCREEN_HEIGHT/2, IMAGE_DICT["game_over"], screen)
                end_title_frame_count += 1
                if end_title_frame_count/FPS >= end_title_seconds:

                    running = False
        elif not player_alive and player_win:
            if frames_since_player_win/FPS > delay_after_player_win:

                imageloader.show_image_centre_snap(
                    SCREEN_WIDTH/2, SCREEN_HEIGHT/2, IMAGE_DICT["you_win"], screen)
                end_title_frame_count += 1
                if end_title_frame_count/FPS >= end_title_seconds:

                    running = False

        pygame.display.update()
        CLOCK.tick(FPS)


level_one(running)
