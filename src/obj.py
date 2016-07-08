from pygame import Rect


class Obj:
    def __init__(self, x, y, size_x, size_y):
        self.rect = Rect(x, y, size_x, size_y)
        self.img = None

    def render(self, screen, update_queue):
        screen.blit(self.img, self.rect)

        update_queue.append(self.rect)
