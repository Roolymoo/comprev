from pygame import draw

class Player:
    def __init__(self, bond_x, bond_y):
        self.x = 0
        self.y = 0
        self.bond_x = bond_x
        self.bond_y = bond_y
        self.radius = 30
        self.mov_unit = 15

    def move_left(self):
        if self.x > self.mov_unit:
            self.x -= self.mov_unit

    def move_right(self):
        if self.x < self.bond_x - self.mov_unit:
            self.x += self.mov_unit

    def move_up(self):
        if self.y > self.mov_unit:
            self.y -= self.mov_unit

    def move_down(self):
        if self.y < self.bond_y - self.mov_unit:
            self.y += self.mov_unit

    def render(self, screen):
        blue = (30, 144, 255)

        draw.circle(screen, blue, (self.x, self.y), self.radius)