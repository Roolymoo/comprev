from operator import add, sub, gt, lt

from pygame import Rect

from collision import is_collides


def _move(bot, dir, *args):
    """args is one or more iterables that each contains objects. Returns False if there is an
    such an obj which blocks self from moving in direction dir, otherwise return True and
    have bot's position updated."""
    rect = bot.rect.copy()
    if dir == "left":
        rect.x -= bot.mov_unit
    elif dir == "right":
        rect.x += bot.mov_unit
    elif dir == "up":
        rect.y -= bot.mov_unit
    elif dir == "down":
        rect.y += bot.mov_unit

    obj = is_collides(rect, *args)
    if obj is None:
        bot.rect = rect
        return True
    else:
        bot.adj_obj = obj
        return False


def _is_clear_shot(lbot, dir, player, *args):
    """Checks if there is no obstruction between lbot and player. If there isn't, a rect is
    loaded into lbot.shot for shooting phase, and True is returned. Otherwise False is
    returned."""
    # TODO: center the laser more. hopefully this fixes the ai stopping oddly to the right of player
    if dir == "left":
        x, y = lbot.rect.x - lbot.mov_unit, lbot.rect.y + lbot.mov_unit
    elif dir == "right":
        x, y = lbot.rect.x + lbot.rect.w, lbot.rect.y + lbot.mov_unit
    elif dir == "up":
        x, y = lbot.rect.x + lbot.mov_unit, lbot.rect.y
    elif dir == "down":
        x, y = lbot.rect.x + lbot.mov_unit, lbot.rect.y + lbot.rect.h

    shot = Rect(x, y, lbot.mov_unit, lbot.rect.y + 2 * lbot.mov_unit)

    d = {"left": [sub, 0, 0, gt], "right": [add, 0, player.bond_x, lt], "up": [sub, 1, 0, gt],
         "down": [add, 1, player.bond_y, lt]}
    op, i, bond, comp = d[dir]

    # try to create the shot
    while not is_collides(shot, *args) and comp(shot[i], bond):
        # grow shot
        shot[i] = op(shot[i], player.mov_unit)

    if shot.colliderect(player.rect):
        lbot.shot = shot
        return True
    else:
        return False


class CaptureBot:
    """Tries to contact (capture) player (be in within 0 pixels in some direction from player)."""

    def __init__(self, x, y, size):
        self.rect = Rect(x, y, size, size)
        self.img = None
        self.mov_unit = int(size / 25)
        # Most recently collided into object
        self.adj_obj = None

    def move(self, player, *args):
        """args is a collection of iterables each containing objects. Moves closer to player's
        current location."""
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


class LaserBot(CaptureBot):
    def __init__(self, x, y, size):
        CaptureBot.__init__(self, x, y, size)
        # Contains rect that is shot if a shot can be made
        self.shot = None

    def move(self, player, *args):
        """Moves only to get clear shot at player"""
        p_x = player.rect.x
        p_y = player.rect.y
        b_x = self.rect.x
        b_y = self.rect.y

        # check for a clear shot. if there is one, saves it for shooting phase, doesnt move
        if p_x < b_x:
            if _is_clear_shot(self, "left", player, [player], *args):
                return
        if p_x > b_x:
            if _is_clear_shot(self, "right", player, [player], *args):
                return
        if p_y < b_y:
            if _is_clear_shot(self, "up", player, [player], *args):
                return
        if p_y > b_y:
            if _is_clear_shot(self, "down", player, [player], *args):
                return

        # no clear shot, move closer to player instead
        CaptureBot.move(self, player, *args)
