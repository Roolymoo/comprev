from collections import deque
import os.path

import pygame
from pygame.locals import QUIT, KEYDOWN, K_a, K_s, K_d, K_w, KEYUP, K_p
from pygame import time, transform

from render import update_display
from player import Player
from background import Background
from level import load_level
from collision import is_collides
from monsters import CaptureBot, LaserBot, PatrolBot


def _is_killed_all(monster_list):
    """does not count PatrolBots."""
    count = 0
    for monster in monster_list:
        if type(monster) is not PatrolBot:
            count += 1

    return count == 0


if __name__ == "__main__":
    # init
    running = True
    killed = False

    pygame.init()

    # allow key repeating for holding them down
    # i just pulled these values off internets
    KEY_DELAY = 1
    KEY_INTERVAL = 50
    pygame.key.set_repeat(KEY_DELAY, KEY_INTERVAL)

    fps_clock = pygame.time.Clock()
    FPS = 30

    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 700

    TILE_SIZE = 50

    # Mouse button codes (pygame specific)
    LEFT_MB = 1

    # Colours
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (211, 211, 211)

    # Art
    PLAYER_N = "man_standing3.png"
    GBG_CAN_N = "garbage_can.png"
    COMP_SAD_N = "computer_sad.png"
    COMP_HAP_N = "computer_happy.png"
    CUB_MED_N = "cubicle_med.png"
    CUB_MED_COM_N = "cubicle_med_computer_happy.png"
    LEVEL1_N = "level1.txt"

    # music
    MUSIC_DIR = "music"
    MUSIC_N = "robotpoop (ai)_v2-01.ogg"

    # Create the screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # put desks, garbage cans, etc in here
    env_obj_list = deque()

    # put the ai stuff in here, but not player
    monster_list = deque()

    # init rendering
    update_queue = deque() # Queue of rects specifying areas of display to update

    background = Background(WINDOW_WIDTH, WINDOW_HEIGHT, GREY)
    background.render(screen, update_queue)

    # load level
    # portal is rect of where the player has to get to after killing all computer's to advance to next level
    player, portal, env_obj_list, monster_list = load_level(os.path.join("levels", LEVEL1_N), TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, background, screen, update_queue)

    # # DEBUG LEVEL
    # # draw a bunch of garbage cans (debug)
    # x_coord = TILE_SIZE * 3
    # while x_coord < TILE_SIZE * 10:
    #     y_coord = TILE_SIZE * 3
    #     while y_coord < WINDOW_HEIGHT:
    #         gbg_can = Obj(x_coord, y_coord, TILE_SIZE, TILE_SIZE)
    #         gbg_can.img = load_img(GBG_CAN_N)
    #         gbg_can.render(screen, update_queue)
    #
    #         env_obj_list.append(gbg_can)
    #
    #         y_coord += TILE_SIZE * 2
    #
    #     x_coord += TILE_SIZE * 2
    #
    #
    # # create a capture bot (debug)
    # cbot = CaptureBot(WINDOW_WIDTH - TILE_SIZE, WINDOW_HEIGHT - TILE_SIZE, TILE_SIZE)
    # cbot.img = load_img(COMP_HAP_N)
    # cbot.render(screen, update_queue)
    #
    # monster_list.append(cbot)
    #
    # # create a laser bot (debug)
    # lbot = LaserBot(WINDOW_WIDTH - TILE_SIZE, TILE_SIZE * 3, TILE_SIZE)
    # lbot.img = load_img(COMP_SAD_N)
    # lbot.render(screen, update_queue)
    #
    # monster_list.append(lbot)

    # variable for reference to deque of destroyed monsters
    destroyed = None

    # bombs
    bomb_list = deque()

    # Force update display (generally handled at end of main loop below)
    update_display(update_queue)

    # music!
    pygame.mixer.music.load(os.path.join(MUSIC_DIR, MUSIC_N))
    # play indefinitely
    pygame.mixer.music.play(-1)

    while running and (not killed):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key in (K_a, K_d, K_w, K_s):
                    # player to be moved, clear old location
                    background.render(screen, update_queue, player.rect.copy())

                    rect = player.rect.copy()
                    if event.key == K_a:
                        rect.x -= player.mov_unit
                        if is_collides(rect, env_obj_list, monster_list) is None:
                            player.move_left()
                    elif event.key == K_d:
                        rect.x += player.mov_unit
                        if is_collides(rect, env_obj_list, monster_list) is None:
                            player.move_right()
                    elif event.key == K_w:
                        rect.y -= player.mov_unit
                        if is_collides(rect, env_obj_list, monster_list) is None:
                            player.move_up()
                    elif event.key == K_s:
                        rect.y += player.mov_unit
                        if is_collides(rect, env_obj_list, monster_list) is None:
                            player.move_down()
            elif event.type == KEYUP and event.key == K_p:
                # player left poop bomb!
                bomb_list.append(player.drop_bomb(FPS))
            elif event.type == QUIT:
                running = False

            player.render(screen, update_queue)

        # monster ai
        for monster in monster_list:
            # clear old location
            background.render(screen, update_queue, monster.rect.copy())

            # remove this monster from general list when checking collisions
            monster_list_copy = monster_list.__copy__()
            monster_list_copy.remove(monster)

            if type(monster) is PatrolBot:
                monster.move([player], env_obj_list, monster_list_copy)
            elif type(monster) is CaptureBot:
                monster.move(player, env_obj_list, monster_list_copy)
            elif type(monster) is LaserBot:
                monster.move(player, env_obj_list, monster_list_copy)

            monster.render(screen, update_queue)

            # Check if player died
            if ((type(monster) is CaptureBot) or (type(monster) is PatrolBot)) and type(monster.adj_obj) is Player:
                killed = True
            if type(monster) is LaserBot and (monster.shot is not None):
                killed = True

        # copy bomb list so can remove bomb's from original list when they explode (can't remove things from a deque
        # while you are iterating it)
        bomb_list_c = bomb_list.__copy__()
        for bomb in bomb_list_c:
            if not bomb.is_explode():
                bomb.render(screen, update_queue)
            else:
                # remove from screen
                background.render(screen, update_queue, bomb.rect.copy())

                bomb_list.remove(bomb)
                bomb_mess, destroyed = bomb.explode(monster_list)
                bomb_mess.render(screen, update_queue)
                background.obj_list.append(bomb_mess)

        # re-render any player or monster intersecting any bomb's rect so they are rendered on top
        if is_collides(player.rect, bomb_list):
            player.render(screen, update_queue)
        for monster in monster_list:
            if is_collides(monster.rect, bomb_list):
                monster.render(screen, update_queue)

        # remove any destroyed monsters
        if destroyed is not None:
            for monster in destroyed:
                monster_mess = monster.on_death()
                monster_mess.render(screen, update_queue)
                background.obj_list.append(monster_mess)

                monster_list.remove(monster)

                # remove from screen
                background.render(screen, update_queue, monster.rect.copy())

            destroyed = None

        # check if player advanced to next level (at portal and killed all bots)
        if player.rect.colliderect(portal.rect) and _is_killed_all(monster_list):
            time.wait(2000)
            # reset environment
            background.reset()
            background.render(screen, update_queue)
            player, portal, env_obj_list, monster_list = load_level(os.path.join("levels", LEVEL1_N), TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, background, screen, update_queue)

        update_display(update_queue)

        fps_clock.tick(FPS)

    if killed:
        # freeze for a sec so player can see how they died (e.g. see laser rendered for a bit)
        time.wait(2000)
