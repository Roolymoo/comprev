from pygame import Rect, time

from img import load_img
from collision import is_collides


class Bomb:
    """Note that Bomb will not have collision detection. Player and NPCs can move over it and will render over top.
    Bomb's will be handled in a separate loop for rendering to ensure they don't render over player or NPCs."""
    def __init__(self, rect, fps):
        self.rect = rect
        self.img = load_img("poop_bomb.png")
        self.fps = fps
        # how long until bomb explodes
        # TODO: allow player to input # after lifting up from P to specify timer?
        self.expl_time = 5000
        # time past since bomb creation
        self.time = 0
        self.clock = time.Clock()

    def explode(self):
        """Returns True if enough time has passed for explode, otherwise False, but the clock will be updated in
        either case."""
        self.time += self.clock.tick(self.fps)
        return self.time >= self.expl_time

    def render(self, screen, update_queue):
        screen.blit(self.img, self.rect)

        update_queue.append(self.rect)
