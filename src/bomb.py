from collections import deque
import os.path

from pygame import Rect, time, mixer

from img import load_img
from monsters import PatrolBot


class BombMess:
    def __init__(self, rect):
        self.rect = rect
        self.img = load_img("bomb_mess.png")

    def render(self, screen, update_queue):
        screen.blit(self.img, self.rect)

        update_queue.append(self.rect)


class Bomb:
    """Note that Bomb will not have collision detection. Player and NPCs can move over it and will render over top.
    Bomb's will be handled in a separate loop for rendering to ensure they don't render over player or NPCs."""
    def __init__(self, rect, fps):
        self.rect = rect
        self.img = load_img("poop_bomb.png")
        self.noise = mixer.Sound(os.path.join("sounds", "explosion_soft.wav"))
        self.fps = fps
        # how long until bomb explodes
        self.expl_time = 4000
        # time past since bomb creation
        self.time = 0
        self.clock = time.Clock()

    def is_explode(self):
        """Returns True if enough time has passed for explode, otherwise False, but the clock will be updated in
        either case."""
        self.time += self.clock.tick(self.fps)
        return self.time >= self.expl_time

    def explode(self, monster_list):
        """Checks immediately adjacent tiles for monsters, if there are any they are added to a deque object.
        Returns a BombMess object along with the deque. Play's bomb noise."""
        x, y, w, h = self.rect
        collis_rect = Rect(x - w, y - h, 3 * w, 3 * h)
        destroyed = deque()
        for monster in monster_list:
            if monster.rect.colliderect(collis_rect) and type(monster) is not PatrolBot:
                destroyed.append(monster)

        self.noise.play()

        return BombMess(self.rect.copy()), destroyed

    def render(self, screen, update_queue):
        screen.blit(self.img, self.rect)

        update_queue.append(self.rect)
