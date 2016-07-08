from pygame import draw, Rect


class Player:
    def __init__(self, bond_x, bond_y, size_x, size_y):
        # rect contains player
        self.rect = Rect(0, 0, size_x, size_y)
        self.bond_x = bond_x - self.rect.w
        self.bond_y = bond_y - self.rect.h
        self.mov_unit_x = int(size_x / 2.5)
        self.mov_unit_y = int(size_y / 5)
        self.img = None

    def move_left(self):
        if self.rect.x > self.mov_unit_x:
            self.rect.x -= self.mov_unit_x

    def move_right(self):
        if self.rect.x < self.bond_x - self.mov_unit_x:
            self.rect.x += self.mov_unit_x

    def move_up(self):
        if self.rect.y > self.mov_unit_y:
            self.rect.y -= self.mov_unit_y

    def move_down(self):
        if self.rect.y < self.bond_y - self.mov_unit_y:
            self.rect.y += self.mov_unit_y

    def render(self, screen, update_queue):
        screen.blit(self.img, self.rect)

        update_queue.append(self.rect)