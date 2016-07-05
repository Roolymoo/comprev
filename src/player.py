from pygame import draw, Rect


class Player:
    def __init__(self, bond_x, bond_y):
        # rect contains player
        self.rect = Rect(0, 0, 60, 60)
        self.bond_x = bond_x - self.rect.w
        self.bond_y = bond_y - self.rect.h
        self.mov_unit = 15

    def move_left(self):
        if self.rect.x > self.mov_unit:
            self.rect.x -= self.mov_unit

    def move_right(self):
        if self.rect.x < self.bond_x - self.mov_unit:
            self.rect.x += self.mov_unit

    def move_up(self):
        if self.rect.y > self.mov_unit:
            self.rect.y -= self.mov_unit

    def move_down(self):
        if self.rect.y < self.bond_y - self.mov_unit:
            self.rect.y += self.mov_unit

    def render(self, screen, update_queue):
        blue = (30, 144, 255)

        draw.rect(screen, blue, self.rect)

        update_queue.append(self.rect)