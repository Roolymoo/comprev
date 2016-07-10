from collections import deque

import pygame
from pygame.locals import QUIT, KEYDOWN, K_a, K_s, K_d, K_w
from pygame import time

from render import update_display
from player import Player
from background import Background
from obj import Obj
from img import load_img
from collision import is_collides
from monsters import CaptureBot, LaserBot


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
    GBG_CAN_N = "garbage_can.png"
    COMP_SAD_N = "computer_sad.png"
    COMP_HAP_N = "computer_happy.png"

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

    # draw a bunch of garbage cans (debug)
    x_coord = TILE_SIZE * 3
    while x_coord < TILE_SIZE * 10:
        y_coord = TILE_SIZE * 3
        while y_coord < WINDOW_HEIGHT:
            gbg_can = Obj(x_coord, y_coord, TILE_SIZE)
            gbg_can.img = load_img(GBG_CAN_N)
            gbg_can.render(screen, update_queue)

            env_obj_list.append(gbg_can)

            y_coord += TILE_SIZE * 2

        x_coord += TILE_SIZE * 2

    # Draw player (debug)
    player = Player(WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE)
    player.img = load_img(COMP_SAD_N)
    player.render(screen, update_queue)

    # create a capture bot (debug)
    cbot = CaptureBot(WINDOW_WIDTH - TILE_SIZE, WINDOW_HEIGHT - TILE_SIZE, TILE_SIZE)
    cbot.img = load_img(COMP_HAP_N)
    cbot.render(screen, update_queue)

    monster_list.append(cbot)

    # create a laser bot (debug)
    lbot = LaserBot(WINDOW_WIDTH - TILE_SIZE, TILE_SIZE * 3, TILE_SIZE)
    lbot.img = load_img(COMP_HAP_N)
    lbot.render(screen, update_queue)

    monster_list.append(lbot)

    # Force update display (generally handled at end of main loop below)
    update_display(update_queue)

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

            monster.move(player, env_obj_list, monster_list_copy)

            monster.render(screen, update_queue)

            # Check if player died
            if type(monster) is CaptureBot and isinstance(monster.adj_obj, Player):
                killed = True
            if type(monster) is LaserBot and (monster.shot is not None):
                killed = True

        update_display(update_queue)

        fps_clock.tick(FPS)

    if killed:
        # freeze for a sec so player can see how they died (e.g. see laser rendered for a bit)
        time.wait(2000)
