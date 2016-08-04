from collections import deque
import os.path

import pygame
from pygame.locals import QUIT, KEYDOWN, K_a, K_s, K_d, K_w, KEYUP, K_p, K_ESCAPE, K_y, K_n, K_g
from pygame import time, font, Rect, display, mixer
from img import load_img

from render import update_display
from player import Player
from background import Background
from level import load_level
from collision import is_collides
from monsters import CaptureBot, LaserBot, PatrolBot, WaitBot, PatrolLaserBot, Boss
from events import Spawner

from random import shuffle, randint

def _is_killed_all(monster_list):
    """does not count PatrolBots."""
    count = 0
    for monster in monster_list:
        if type(monster) is not PatrolBot:
            count += 1

    return count == 0


def _load_level(level):
    background.reset()
    background.render(screen, update_queue)
    player, portal, env_obj_list, monster_list, spawner_list = load_level(os.path.join("levels", level_dict[level]), TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, background, screen, update_queue)
    # bad fix to ensure player renders on top of any background object
    if player:
        player.render(screen, update_queue)
    return player, portal, env_obj_list, monster_list, spawner_list


def update_image(mover, new_image, new_name):
    mover.img = new_image
    mover.img_name = new_name

def shake_screen(screen):
    blank_screen = screen.copy()
    blank_screen.fill((0,0,0))

    screen_copy = screen.copy()

    noise = mixer.Sound(os.path.join("sounds", "explosion_hard1.wav"))

    for i in range(1,500):
        offset = randint(-10,10)
        screen.blit(blank_screen, (0,0))
        screen.blit(screen_copy, (offset,0))
        time.wait(10)
        display.flip()

        # play noise
        if i % 100 == 0:
            noise.play()

    screen.blit(blank_screen, (0,0))
    screen.blit(screen_copy, (0,0))
    display.flip()

if __name__ == "__main__":
    # init
    running = True
    killed = False
    won = False

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

    BOMB_LIMIT = 3

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
    BOSS_LEVEL_N = "boss_level.txt"
    STRT_SCRN_N = "startscreen.txt"
    INTRO_SCRN_N = "intro_level.txt"

    # Animation Prerendered Surfaces
    PLAYER_RIGHT_1 = load_img("man_2_right1.png")
    PLAYER_RIGHT_2 = load_img("man_2_right2.png")
    PLAYER_LEFT_1 = load_img("man_2_left1.png")
    PLAYER_LEFT_2 = load_img("man_2_left2.png")
    move_count = 0

    CHASEBOT_LEFT = load_img("chasebot_l.png")
    CHASEBOT_RIGHT = load_img("chasebot_r.png")

    DOOR_OPEN = load_img("door_open.png")
    DOOR_CLOSED = load_img("door_closed.png")

    BOSS_SMILE = load_img("boss_smile.png")
    BOSS_SHIELD = load_img("boss_smile_shield.png")

    BOSS_SMILE2 = load_img("boss_smile2.png")
    BOSS_SHIELD2 = load_img("boss_shield2.png")

    # clocks for doors
    door_times = [0, 0, 0, 0]
    door_clocks = [None, None, None, None]

    # music
    MUSIC_DIR = "music"
    MUSIC_N = "robotpoop (ai)_v2-01.ogg"
    MUSIC_BOSS_N = "robotpoop (boss)_v1.ogg"

    # Create the screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # put desks, garbage cans, etc in here
    env_obj_list = deque()

    # put the ai stuff in here, but not player
    monster_list = deque()

    # init rendering
    update_queue = deque() # Queue of rects specifying areas of display to update

    background = Background(WINDOW_WIDTH, WINDOW_HEIGHT, GREY)

    # levels
    level_dict = {0: STRT_SCRN_N, 1: INTRO_SCRN_N, 2: LEVEL1_N, 3: BOSS_LEVEL_N}
    # load start screen
    level = 3

    # portal is rect of where the player has to get to after killing all computer's to advance to next level
    player, portal, env_obj_list, monster_list, spawner_list = _load_level(level)

    # variable for reference to deque of destroyed monsters
    destroyed = None

    # bombs
    bomb_ctr = 0
    bomb_list = deque()

    # Force update display (generally handled at end of main loop below)
    update_display(update_queue)

    music_loaded = False
    music_advance = False

    # for player pausing game
    pause = False
    # for toggling pause at end of main loop
    unpause = False

    if level in (0, 1):
        # prevent certain unwanted processes for running
        pause = True

    while running and (not killed):
        # music
        if level == 2 and not music_loaded:

            pygame.mixer.music.load(os.path.join(MUSIC_DIR, MUSIC_N))

            # play indefinitely
            pygame.mixer.music.play(-1)
            # need variable, seems API get_busy doesn't consider paused as not busy
            music_pause = False

            music_loaded = True

        if level == 3 and not music_loaded:

            # stop whatever music that is playing
            pygame.mixer.music.stop()

            # load new music
            pygame.mixer.music.load(os.path.join(MUSIC_DIR, MUSIC_BOSS_N))


            # play indefinitely
            pygame.mixer.music.play(-1)
            # need variable, seems API get_busy doesn't consider paused as not busy
            music_pause = False

            music_loaded = True

        # ~~~~possibly deprecated
        # # events
        # for event in spawner_list:
        #     if type(event) is Spawner:
        #         if not event.is_spawned:
        #             event.spawn(monster_list, screen, update_queue)

        # input loop
        for event in pygame.event.get():
            if level == 3 and music_advance:
                pygame.mixer.music.load(os.path.join(MUSIC_DIR, MUSIC_BOSS_N))
                pygame.mixer.music.play(-1)
                music_advance = False

            if level == 4:
                #Do stuff
                pass

            if event.type == KEYDOWN:
                # ~~~~~DEBUG ONLY~~~~~~~~~~~~~~
                if event.key == K_g:
                    destroyed = monster_list.__copy__()
                elif event.key and level == 1:
                    # load next level, first level with enemies
                    level += 1
                    unpause = True
                    player, portal, env_obj_list, monster_list, spawner_list = _load_level(level)
                elif event.key in (K_a, K_d, K_w, K_s) and not pause:
                    # player to be moved, clear old location
                    background.render(screen, update_queue, player.rect.copy())

                    rect = player.rect.copy()
                    if event.key == K_a:
                        rect.x -= player.mov_unit
                        if is_collides(rect, env_obj_list, monster_list) is None:
                            player.move_left()

                            if player.img_name != ("LEFT1" or "LEFT2"):
                                player.update_image(PLAYER_LEFT_1, "LEFT1")
                            elif player.img_name != ("LEFT2"):
                                player.update_image(PLAYER_LEFT_2, "LEFT2")
                            else:
                                player.update_image(PLAYER_LEFT_1, "LEFT1")

                    elif event.key == K_d:
                        rect.x += player.mov_unit
                        if is_collides(rect, env_obj_list, monster_list) is None:
                            player.move_right()

                            if player.img_name != ("RIGHT1" or "RIGHT2"):
                                player.update_image(PLAYER_RIGHT_1, "RIGHT1")
                            elif player.img_name != ("RIGHT2"):
                                player.update_image(PLAYER_RIGHT_2, "RIGHT2")
                            else:
                                player.update_image(PLAYER_RIGHT_1, "RIGHT1")


                    elif event.key == K_w:
                        rect.y -= player.mov_unit
                        if is_collides(rect, env_obj_list, monster_list) is None:
                            player.move_up()
                    elif event.key == K_s:
                        rect.y += player.mov_unit
                        if is_collides(rect, env_obj_list, monster_list) is None:
                            player.move_down()

                    player.render(screen, update_queue)

            elif event.type == KEYUP:
                if event.key == K_p and not pause:

                    # player left poop bomb!
                    if bomb_ctr < BOMB_LIMIT:
                        bomb_list.append(player.drop_bomb(FPS))
                        bomb_ctr += 1
                elif event.key == K_ESCAPE and not (level in (0, 1, 4)):
                    # toggle
                    pause = not pause
                    if music_pause:
                        pygame.mixer.music.unpause()
                        music_pause = False
                    else:
                        pygame.mixer.music.pause()
                        music_pause = True
                elif event.key == K_y and level == 0:
                    # load next level
                    level += 1
                    player, portal, env_obj_list, monster_list, spawner_list = _load_level(level)
                elif event.key == K_n and level == 0:
                    # quit game from start menu
                    running = False
            elif event.type == QUIT:
                running = False

        if not pause:
            # close trapdoors if necessary
            for trapdoor in spawner_list:
                if trapdoor.is_open:
                    trapdoor.time += trapdoor.clock.tick(FPS)

                    if trapdoor.time > 2000:

                        # remove current trapdoor
                        background.render(screen, update_queue, trapdoor.rect.copy())

                        trapdoor.close()
                        trapdoor.render(screen, update_queue)

            # monster ai
            for monster in monster_list:
                # clear old location
                background.render(screen, update_queue, monster.rect.copy())

                # remove this monster from general list when checking collisions
                monster_list_copy = monster_list.__copy__()
                monster_list_copy.remove(monster)

                monster.move(player, env_obj_list, monster_list_copy)

                if type(monster) in (PatrolBot, CaptureBot):
                    # update image
                    if monster.move_count > 1:
                        update_image(monster, CHASEBOT_LEFT, "left")
                        monster.move_count = 0
                    else:
                        update_image(monster, CHASEBOT_RIGHT, "right")
                if type(monster) is WaitBot and monster.sighted:
                    # update image
                    if monster.move_count > 1:
                        update_image(monster, CHASEBOT_LEFT, "left")
                        monster.move_count = 0
                    else:
                        update_image(monster, CHASEBOT_RIGHT, "right")

                if type(monster) is Boss:
                    if monster.shield:
                        monster.time += monster.clock.tick(monster.fps)

                        # Check if shield should be turned off
                        if monster.time > monster.shield_time:
                            monster.shield_off()

                            if monster.hp < 5:
                                update_image(monster, BOSS_SMILE2, "smile")
                            else:
                                update_image(monster, BOSS_SMILE, "smile")

                monster.render(screen, update_queue)

                # Check if player died
                if type(monster) in (CaptureBot, WaitBot, PatrolBot) and type(monster.adj_obj) is Player:
                    killed = True
                if type(monster) in (LaserBot, PatrolLaserBot) and (monster.shot is not None):
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
                    bomb_ctr -= 1
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

                    # spawn monsters
                    if type(monster) is Boss:
                        if not monster.shield:
                            monster.hp -= 1

                            if monster.hp == 9:
                                spawn_list = [0]

                            elif monster.hp >=7 and monster.hp <= 8:
                                spawn_list = [0,1]

                            elif monster.hp >= 4 and monster.hp <= 6:
                                spawn_list = [0,1,2]

                            elif monster.hp >= 2 and monster.hp <= 3:
                                spawn_list = [0,1,2,3]
                                shuffle(spawn_list)
                                spawn_list = spawn_list[0:3]

                            elif monster.hp == 1:
                                spawn_list = [0,1,2,3]

                            else:
                                spawn_list = []

                            # spawn monsters and open doors
                            for i in spawn_list:

                                # remove current trapdoor
                                background.render(screen, update_queue, spawner_list[i].rect.copy())

                                spawner_list[i].open()
                                spawner_list[i].render(screen, update_queue)
                                spawner_list[i].spawner.spawn(monster_list, screen, update_queue)

                            if monster.hp < 1:

                                # initiate explosion sequence
                                pygame.mixer.music.fadeout(2000)
                                shake_screen(screen)

                                monster_list.remove(monster)

                                level += 1

                            else:

                                # check if fps has been set to a variable
                                if monster.fps == None:
                                    monster.fps = FPS

                                monster.shield_on()

                                if monster.hp < 5:
                                    update_image(monster, BOSS_SHIELD2, "shield")
                                else:
                                    update_image(monster, BOSS_SHIELD, "shield")


                            # remove from screen
                            background.render(screen, update_queue, monster.rect.copy())
                    else:
                        monster_mess = monster.on_death()
                        monster_mess.render(screen, update_queue)
                        background.obj_list.append(monster_mess)

                        monster_list.remove(monster)
                        # remove monster from a spawner if it came from one
                        for event in spawner_list:
                            if type(event) is Spawner:
                                if event.contains(monster):
                                    event.remove(monster)

                        # remove from screen
                        background.render(screen, update_queue, monster.rect.copy())

                destroyed = None

            # check if player advanced to next level (at portal and killed all bots)
            if portal and player.rect.colliderect(portal.rect) and _is_killed_all(monster_list):
                # time.wait(2000)
                if level == 2:
                    pygame.mixer.music.fadeout(2000)
                time.wait(2000)
                level += 1
                player, portal, env_obj_list, monster_list, spawner_list = _load_level(level)
                music_advance = True

            # check if player won
            if level == 3 and _is_killed_all(monster_list):
                pygame.mixer.music.fadeout(2000)
                time.wait(2000)
                level += 1
                player, portal, env_obj_list, monster_list, spawner_list = _load_level(level)
                won = True
                running = False

        update_display(update_queue)

        fps_clock.tick(FPS)

        if unpause:
            pause = False
            unpause = False

    if killed:
        # freeze for a sec so player can see how they died (e.g. see laser rendered for a bit)
        time.wait(2000)
    elif won:
        # Let player hit a key to quit game when they are ready
        running = True
        while running:
             for event in pygame.event.get():
                 if event.key:
                     running = False
