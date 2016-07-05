from collections import deque

import pygame
from pygame import display
from pygame import draw
from pygame.locals import QUIT, KEYDOWN, K_a, K_s, K_d, K_w

import collision
from player import Player


def update_display(update_queue):
    """(deque) -> NoneType
    Updates display with Rects given in update_queue, and clears update_queue."""
    display.update(update_queue)

    update_queue.clear()

def clear(screen, obj_list, obj, update_queue):
    """(Surface, list, *, deque) -> NoneType
    For each obj in obj_list that obj overlaps with, call their render() method."""
    for elem in obj_list:
        if collision.is_collides(elem, obj):
            elem.render(screen, update_queue)


if __name__ == "__main__":
    # init
    running = True

    pygame.init()

    # allow key repeating for holding them down
    # these values right?
    KEY_DELAY = 1
    KEY_INTERVAL = 50
    pygame.key.set_repeat(KEY_DELAY, KEY_INTERVAL)

    fps_clock = pygame.time.Clock()
    FPS = 20

    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 840

    # Mouse button codes (pygame specific)
    LEFT_MB = 1

    # Colours
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (211, 211, 211)

    # Create the screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # init rendering
    update_queue = deque() # Queue of rects specifying areas of display to update

    screen.fill(GREY)

    # Draw grid (debug)
    # 60x60 tiles, 20 x 14 tiles
    size = 60
    # vertical lines
    x_coord = size
    while x_coord < WINDOW_WIDTH:
        draw.line(screen, WHITE, (x_coord, 0), (x_coord, WINDOW_HEIGHT))
        x_coord += size
    # horizontal lines
    y_coord = size
    while y_coord < WINDOW_HEIGHT:
        draw.line(screen, WHITE, (0, y_coord), (WINDOW_WIDTH, y_coord))
        y_coord += size

    # Draw player (debug)
    player = Player(WINDOW_WIDTH,WINDOW_HEIGHT)
    player.render(screen)

    # Force update display (generally handled at end of main loop below)
    display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_a:
                    player.move_left()
                elif event.key == K_d:
                    player.move_right()
                elif event.key == K_w:
                    player.move_up()
                elif event.key == K_s:
                    player.move_down()
            elif event.type == QUIT:
                running = False

            player.render(screen)

            display.flip()

            # update_display(update_queue)

        fps_clock.tick(FPS)
