from collections import deque

import pygame
from pygame.locals import QUIT, KEYDOWN, K_a, K_s, K_d, K_w

from render import update_display
from player import Player
from background import Background
from obj import Obj
from img import load_img, load_sizes
from collision import is_collides
from monsters import CaptureBot


if __name__ == "__main__":
    # init
    running = True

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
    IMG_SIZES = load_sizes("sizes.txt")
    GBG_CAN_N = "garbage_can.png"
    COMP_SAD_N = "computer_sad.png"
    COMP_HAP_N = "computer_happy.png"

    # Create the screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    env_obj_list = deque()

    monster_list = deque()

    # init rendering
    update_queue = deque() # Queue of rects specifying areas of display to update

    background = Background(WINDOW_WIDTH, WINDOW_HEIGHT, GREY)
    background.render(screen, update_queue)

    # draw a bunch of garbage cans (debug)
    gbg_can_size = IMG_SIZES["garbage_can"]

    x_coord = TILE_SIZE * 3
    while x_coord < TILE_SIZE * 10:
        y_coord = TILE_SIZE * 3
        while y_coord < WINDOW_HEIGHT:
            gbg_can = Obj(x_coord, y_coord, gbg_can_size[0], gbg_can_size[1])

            gbg_can.img = load_img(GBG_CAN_N)
            gbg_can.render(screen, update_queue)

            env_obj_list.append(gbg_can)

            y_coord += TILE_SIZE * 2

        x_coord += TILE_SIZE * 2

    # Draw player (debug)
    player_size = IMG_SIZES["computer_sad"]
    player = Player(WINDOW_WIDTH, WINDOW_HEIGHT, player_size[0], player_size[1])
    player.img = load_img(COMP_SAD_N)
    player.render(screen, update_queue)

    # create a capture bot (debug)
    cbot = CaptureBot(WINDOW_WIDTH - TILE_SIZE, WINDOW_HEIGHT - TILE_SIZE, TILE_SIZE,
                      WINDOW_WIDTH, WINDOW_HEIGHT)
    cbot.img = load_img(COMP_HAP_N)
    cbot.render(screen, update_queue)

    monster_list.append(cbot)

    # Force update display (generally handled at end of main loop below)
    update_display(update_queue)

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key in (K_a, K_d, K_w, K_s):
                    # player to be moved, clear old location
                    background.render(screen, update_queue, player.rect.copy())

                    rect = player.rect.copy()
                    if event.key == K_a:
                        rect.x -= player.mov_unit_x
                        if not is_collides(rect, env_obj_list, monster_list):
                            player.move_left()
                    elif event.key == K_d:
                        rect.x += player.mov_unit_x
                        if not is_collides(rect, env_obj_list, monster_list):
                            player.move_right()
                    elif event.key == K_w:
                        rect.y -= player.mov_unit_y
                        if not is_collides(rect, env_obj_list, monster_list):
                            player.move_up()
                    elif event.key == K_s:
                        rect.y += player.mov_unit_y
                        if not is_collides(rect, env_obj_list, monster_list):
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

        update_display(update_queue)

        fps_clock.tick(FPS)
