from pygame import Rect


class Obj:
    def __init__(self, x, y, w, h):
        self.rect = Rect(x, y, w, h)
        self.img = None

    def render(self, screen, update_queue):
        screen.blit(self.img, self.rect)

        update_queue.append(self.rect)
