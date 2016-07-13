from collections import deque
import os.path

import pygame
from pygame.locals import QUIT, KEYDOWN, K_a, K_s, K_d, K_w, KEYUP, K_p
from pygame import time, transform

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
    PLAYER_N = "man_standing3.png"
    GBG_CAN_N = "garbage_can.png"
    COMP_SAD_N = "computer_sad.png"
    COMP_HAP_N = "computer_happy.png"
    CUB_MED_N = "cubicle_med.png"
    CUB_MED_COM_N = "cubicle_med_computer_happy.png"

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

    # Draw player
    player = Player(WINDOW_WIDTH - TILE_SIZE, WINDOW_HEIGHT - TILE_SIZE, WINDOW_WIDTH,
                    WINDOW_HEIGHT, TILE_SIZE)
    player.img = load_img(PLAYER_N)
    player.render(screen, update_queue)

    # level (inspired from http://cdn2.business2community.com/wp-content/uploads/2012/10/Officelayout-600x386.jpg)
    # bottom
    cub = Obj(2 * TILE_SIZE, 9 * TILE_SIZE, 100, 150)
    cub.img = transform.rotate(transform.flip(load_img(CUB_MED_N), False, True), 90)
    cub.render(screen, update_queue)
    env_obj_list.append(cub)

    cub = Obj(4 * TILE_SIZE, 10 * TILE_SIZE, 150, 100)
    cub.img = transform.flip(load_img(CUB_MED_N), False, True)
    cub.render(screen, update_queue)
    env_obj_list.append(cub)

    cub = Obj(7 * TILE_SIZE, 10 * TILE_SIZE, 150, 100)
    cub.img = transform.flip(load_img(CUB_MED_COM_N), False, True)
    cub.render(screen, update_queue)
    env_obj_list.append(cub)

    cub = Obj(10 * TILE_SIZE, 10 * TILE_SIZE, 150, 100)
    cub.img = transform.flip(load_img(CUB_MED_N), False, True)
    cub.render(screen, update_queue)
    env_obj_list.append(cub)

    cub = Obj(13 * TILE_SIZE, 10 * TILE_SIZE, 150, 100)
    cub.img = transform.flip(load_img(CUB_MED_COM_N), False, True)
    cub.render(screen, update_queue)
    env_obj_list.append(cub)

    gbg_can = Obj(16 * TILE_SIZE, 11 * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    gbg_can.img = load_img(GBG_CAN_N)
    gbg_can.render(screen, update_queue)
    env_obj_list.append(gbg_can)

    gbg_can = Obj(4 * TILE_SIZE, 9 * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    gbg_can.img = load_img(GBG_CAN_N)
    gbg_can.render(screen, update_queue)
    env_obj_list.append(gbg_can)

    cbot = CaptureBot(TILE_SIZE, 10 * TILE_SIZE, TILE_SIZE)
    cbot.img = load_img(COMP_HAP_N)
    cbot.render(screen, update_queue)
    monster_list.append(cbot)

    # top-left
    cub = Obj(3 * TILE_SIZE, TILE_SIZE, 100, 150)
    cub.img = transform.rotate(transform.flip(load_img(CUB_MED_COM_N), False, True), 90)
    cub.render(screen, update_queue)
    env_obj_list.append(cub)

    cub = Obj(2 * TILE_SIZE, 4 * TILE_SIZE, 150, 100)
    cub.img = load_img(CUB_MED_N)
    cub.render(screen, update_queue)
    env_obj_list.append(cub)

    cub = Obj(5 * TILE_SIZE, 4 * TILE_SIZE, 100, 150)
    cub.img = transform.rotate(transform.flip(load_img(CUB_MED_N), False, True), -90)
    cub.render(screen, update_queue)
    env_obj_list.append(cub)

    cub = Obj(5 * TILE_SIZE, 2 * TILE_SIZE, 150, 100)
    cub.img = transform.flip(load_img(CUB_MED_N), False, True)
    cub.render(screen, update_queue)
    env_obj_list.append(cub)

    gbg_can = Obj(4 * TILE_SIZE, 6 * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    gbg_can.img = load_img(GBG_CAN_N)
    gbg_can.render(screen, update_queue)
    env_obj_list.append(gbg_can)

    lbot = LaserBot(3 * TILE_SIZE, 6 * TILE_SIZE, TILE_SIZE)
    lbot.img = load_img(COMP_SAD_N)
    lbot.render(screen, update_queue)
    monster_list.append(lbot)

    lbot = LaserBot(6 * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    lbot.img = load_img(COMP_SAD_N)
    lbot.render(screen, update_queue)
    monster_list.append(lbot)

    # top-middle
    cub = Obj(9 * TILE_SIZE, 2 * TILE_SIZE, 150, 100)
    cub.img = transform.flip(load_img(CUB_MED_COM_N), False, True)
    cub.render(screen, update_queue)
    env_obj_list.append(cub)

    cub = Obj(10 * TILE_SIZE, 4 * TILE_SIZE, 100, 150)
    cub.img = transform.rotate(load_img(CUB_MED_N), -90)
    cub.render(screen, update_queue)
    env_obj_list.append(cub)

    cub = Obj(12 * TILE_SIZE, 4 * TILE_SIZE, 150, 100)
    cub.img = load_img(CUB_MED_COM_N)
    cub.render(screen, update_queue)
    env_obj_list.append(cub)

    cub = Obj(12 * TILE_SIZE, TILE_SIZE, 100, 150)
    cub.img = transform.rotate(transform.flip(load_img(CUB_MED_N), False, True), -90)
    cub.render(screen, update_queue)
    env_obj_list.append(cub)

    gbg_can = Obj(12 * TILE_SIZE, 6 * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    gbg_can.img = load_img(GBG_CAN_N)
    gbg_can.render(screen, update_queue)
    env_obj_list.append(gbg_can)

    # top-right
    cub = Obj(16 * TILE_SIZE, 0, 100, 150)
    cub.img = transform.rotate(transform.flip(load_img(CUB_MED_N), False, True), -90)
    cub.render(screen, update_queue)
    env_obj_list.append(cub)

    gbg_can = Obj(17 * TILE_SIZE, 3 * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    gbg_can.img = load_img(GBG_CAN_N)
    gbg_can.render(screen, update_queue)
    env_obj_list.append(gbg_can)

    # right-middle
    cub = Obj(17 * TILE_SIZE, 5 * TILE_SIZE, 150, 100)
    cub.img = transform.flip(load_img(CUB_MED_N), False, True)
    cub.render(screen, update_queue)
    env_obj_list.append(cub)

    cbot = CaptureBot(18 * TILE_SIZE, 4 * TILE_SIZE, TILE_SIZE)
    cbot.img = load_img(COMP_HAP_N)
    cbot.render(screen, update_queue)
    monster_list.append(cbot)

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

            monster.move(player, env_obj_list, monster_list_copy)

            monster.render(screen, update_queue)

            # Check if player died
            if type(monster) is CaptureBot and isinstance(monster.adj_obj, Player):
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

        update_display(update_queue)

        fps_clock.tick(FPS)

    if killed:
        # freeze for a sec so player can see how they died (e.g. see laser rendered for a bit)
        time.wait(2000)
