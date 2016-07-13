from collections import deque

from pygame import Rect, draw


class Background:
    def __init__(self, w, h, colour):
        self.rect = Rect(0, 0, w, h)
        self.colour = colour
        # objs that become part of background (eg messes from bombs)
        self.obj_list = deque()

    def render(self, screen, update_queue, rect=None):
        if rect is None:
            draw.rect(screen, self.colour, self.rect)
            update_queue.append(self.rect)

            for obj in self.obj_list:
                obj.render(screen, update_queue)
        else:
            draw.rect(screen, self.colour, rect)
            update_queue.append(rect)

            for obj in self.obj_list:
                if obj.rect.colliderect(rect):
                    obj.render(screen, update_queue)
