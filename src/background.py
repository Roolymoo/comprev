from pygame import Rect, draw


class Background:
    def __init__(self, w, h, colour):
        self.rect = Rect(0, 0, w, h)
        self.colour = colour

    def render(self, screen, update_queue, rect=None):
        if rect is None:
            rect = self.rect

        draw.rect(screen, self.colour, rect)
        update_queue.append(rect)
