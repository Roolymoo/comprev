from pygame import Rect


class Obj:
    def __init__(self, x, y, size):
        self.rect = Rect(x, y, size, size)
        self.img = None

    def render(self, screen, update_queue):
        screen.blit(self.img, self.rect)

        update_queue.append(self.rect)
