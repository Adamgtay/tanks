import pygame
from game_logic import constants,event_handler,blit_text,level_countdowns,display_ascii
from game_logic.levels import level_one_ascii_units



def level_one(game_running):
    # game loop
    paused=False
    player_x = constants.CENTRE_X
    player_y = constants.CENTRE_Y+150
    player_alive = True
    player_win = False
    countdown_finished = False
    
    # Define movement flags
    move_up, move_down,move_left,move_right = False,False,False,False

    while game_running:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - constants.START_TIME) /1000 # time in seconds

        constants.SCREEN.fill((0, 0,0)) # black background


        if not paused:
            if player_win:
                blit_text.display_text(constants.SCREEN,"YOU WIN",constants.CAPTION_FONT,constants.CENTRE_X,constants.CENTRE_Y,(255,0,0))
            #elif player_alive and not countdown_finished:
                #countdown_finished = level_countdowns.level_one_countdown(elapsed_time)
            elif player_alive: #and countdown_finished:
                display_ascii.display_unit(level_one_ascii_units.player_tank["straight"],(0,200,255),player_x,player_y,-1,4)
                display_ascii.display_unit(level_one_ascii_units.enemy_tank["straight"],(200,0,0),constants.CENTRE_X,constants.CENTRE_Y,-1,4)
                #display_ascii.display_terrain(level_one_ascii_units.terrain["mud"],(200,0,0),0,0,-1,-1 )
                game_running,paused,move_up,move_down,move_left,move_right = event_handler.event_handler_level_one(game_running,paused,move_up,move_down,move_left,move_right)
                player_x,player_y= event_handler.player_movement(player_x,player_y,move_up,move_down,move_left,move_right,constants.PLAYER_HEIGHT,constants.PLAYER_WIDTH,constants.SCREEN_HEIGHT,constants.SCREEN_WIDTH)


                
        elif paused:
            blit_text.display_text(constants.SCREEN,"PAUSED",constants.MAIN_FONT,constants.CENTRE_X,constants.CENTRE_Y,(255,0,0))
            game_running,paused,move_up,move_down,move_left,move_right = event_handler.event_handler_level_one(game_running,paused,move_up,move_down,move_left,move_right)

        



        pygame.display.update() 
        constants.CLOCK.tick(constants.FPS)