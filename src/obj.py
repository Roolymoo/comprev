from pygame import Rect

from img import load_img


class Obj:
    def __init__(self, x, y, w, h):
        self.rect = Rect(x, y, w, h)
        self.img = None

    def render(self, screen, update_queue):
        screen.blit(self.img, self.rect)

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

    def is_open(self):
        return self.is_open

    def open(self):
        self.is_open = True
        self.img = load_img(self.imgs["open"])

    def close(self):
        self.is_open = False
        self.img = load_img(self.imgs["closed"])
