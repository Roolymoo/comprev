from collections import deque

import pygame
from pygame import display
from pygame import draw
from pygame.locals import QUIT, KEYDOWN, K_a, K_s, K_d, K_w

from render import update_display
from player import Player
from background import Background
from obj import Obj
from img import load_img


def _is_collides(rect):
    for obj in env_obj_list:
        if rect.colliderect(obj.rect):
            return True

    return False

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
    FPS = 20

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

    # Create the screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    env_obj_list = deque()

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
                        rect.x -= player.mov_unit
                        if not _is_collides(rect):
                            player.move_left()
                    elif event.key == K_d:
                        rect.x += player.mov_unit
                        if not _is_collides(rect):
                            player.move_right()
                    elif event.key == K_w:
                        rect.y -= player.mov_unit
                        if not _is_collides(rect):
                            player.move_up()
                    elif event.key == K_s:
                        rect.y += player.mov_unit
                        if not _is_collides(rect):
                            player.move_down()
            elif event.type == QUIT:
                running = False

            player.render(screen, update_queue)

            update_display(update_queue)

        fps_clock.tick(FPS)
