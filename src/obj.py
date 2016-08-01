from pygame import Rect, time

from img import load_img


class Obj:
    def __init__(self, x, y, w, h):
        self.rect = Rect(x, y, w, h)
        self.img = None
        self.colour = None

    def render(self, screen, update_queue):
        if self.img:
            screen.blit(self.img, self.rect)
        elif self.colour:
            screen.fill(self.colour, self.rect)

        update_queue.append(self.rect)


class Portal(Obj):
    def __init__(self, x, y, w, h):
        Obj.__init__(self, x, y, w, h)


class TrapDoor(Obj):
    def __init__(self, x, y, w, h):
        Obj.__init__(self, x, y, w, h)
        self.imgs = {"open": None, "closed": None}
        self.is_open = False
        self.spawner = None
        self.time = 0
        self.clock = time.Clock()

    def is_open(self):
        return self.is_open

    def open(self):

        self.is_open = True
        self.img = load_img(self.imgs["open"])

        self.time = 0
        self.clock = time.Clock()

    def close(self):

        self.is_open = False
        self.img = load_img(self.imgs["closed"])

        self.time = 0
        self.clock = time.Clock()
