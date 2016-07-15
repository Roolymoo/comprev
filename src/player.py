from pygame import draw, Rect

from bomb import Bomb


class Player:
    def __init__(self, x, y, w, h, bond_x, bond_y):
        # rect contains player
        self.rect = Rect(x, y, w, h)
        self.bond_x = bond_x - self.rect.w
        self.bond_y = bond_y - self.rect.h
        self.mov_unit = int(w / 5)
        self.img = None
        self.img_name = "STAND"
        
    def update_image(self, new_image, new_name):
        self.img = new_image
        self.img_name = new_name

    def move_left(self):
        if self.rect.x >= self.mov_unit:
            self.rect.x -= self.mov_unit

    def move_right(self):
        if self.rect.x <= self.bond_x - self.mov_unit:
            self.rect.x += self.mov_unit
            
    def move_up(self):
        if self.rect.y >= self.mov_unit:
            self.rect.y -= self.mov_unit

    def move_down(self):
        if self.rect.y <= self.bond_y - self.mov_unit:
            self.rect.y += self.mov_unit

    def drop_bomb(self, fps):
        """Returns Bomb object at self's location."""
        return Bomb(self.rect.copy(), fps)

    def render(self, screen, update_queue):
        screen.blit(self.img, self.rect)

        update_queue.append(self.rect)