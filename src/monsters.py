from pygame import Rect

from collision import is_collides


def _move(cbot, dir, *args):
    """Returns False if there is an obj in obj_list which blocks self from moving in direction
    dir, otherwise return True and have cbot's position updated."""
    rect = cbot.rect.copy()
    if dir == "left":
        rect.x -= cbot.mov_unit
    elif dir == "right":
        rect.x += cbot.mov_unit
    elif dir == "up":
        rect.y -= cbot.mov_unit
    elif dir == "down":
        rect.y += cbot.mov_unit

    if is_collides(rect, *args):
        return False
    else:
        cbot.rect = rect
        return True


class CaptureBot:
    """Tries to contact (capture) player (be in within 0 pixels in some direction from player)."""

    def __init__(self, x, y, size, bond_x, bond_y):
        self.rect = Rect(x, y, size, size)
        self.img = None
        self.mov_unit = int(size / 5)
        self.bond_x = bond_x - self.rect.w
        self.bond_y = bond_y - self.rect.h

    def move(self, player, *args):
        """Moves closer to player's current location."""
        p_x = player.rect.x
        p_y = player.rect.y
        b_x = self.rect.x
        b_y = self.rect.y

        if p_x < b_x:
            if _move(self, "left", [player], *args):
                return
        if p_x > b_x:
            if _move(self, "right", [player], *args):
                return
        if p_y < b_y:
            if _move(self, "up", [player], *args):
                return
        if p_y > b_y:
            if _move(self, "down", [player], *args):
                return

        # doesn't move if it can't get closer to player

    def render(self, screen, update_queue):
        screen.blit(self.img, self.rect)

        update_queue.append(self.rect)
