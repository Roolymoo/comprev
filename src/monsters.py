from pygame import Rect, draw

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
    # create rectangle extending from middle of lbot to edge of screen
    lb_x, lb_y, lb_w, lb_h = lbot.rect.x, lbot.rect.y, lbot.rect.w, lbot.rect.h
    incr_w = int(lb_w / 3)
    incr_h = int(lb_h / 3)
    bond_x = player.bond_x
    bond_y = player.bond_y
    if dir == "left":
        x, y, w, h = 0, lb_y + incr_h, lb_x, incr_h
    elif dir == "right":
        x, y, w, h = lb_x + lb_w, lb_y + incr_h, bond_x - (lb_x + lb_w), incr_h
    elif dir == "up":
        x, y, w, h = lb_x + incr_w, 0, incr_w, lb_y
    elif dir == "down":
        x, y, w, h = lb_x + incr_w, lb_y + lb_h, incr_w, bond_y - (lb_y + lb_h)

    shot = Rect(x, y, w, h)

    if shot.colliderect(player.rect):
        # hit player, modify rect to extend only to player
        p_x, p_y, p_w, p_h = player.rect.x, player.rect.y, player.rect.w, player.rect.h
        if dir == "left":
            shot.x = p_x + p_w
            shot.w -= p_x + p_w
        elif dir == "right":
            shot.w -= bond_x - p_x
        elif dir == "up":
            shot.y = p_y + p_h
            shot.h -= p_y + p_h
        elif dir == "down":
            shot.h -= bond_y - p_y

        if is_collides(shot, *args):
            # obstacles in way, no good (player shouldn't be in args)
            return False
        else:
            # clear, successful shot!
            lbot.shot = shot
            return True


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
            if _is_clear_shot(self, "left", player, *args):
                return
        if p_x > b_x:
            if _is_clear_shot(self, "right", player, *args):
                return
        if p_y < b_y:
            if _is_clear_shot(self, "up", player, *args):
                return
        if p_y > b_y:
            if _is_clear_shot(self, "down", player, *args):
                return

        # no clear shot, move closer to player instead
        CaptureBot.move(self, player, *args)

    def render(self, screen, update_queue):
        # self
        screen.blit(self.img, self.rect)
        # shot, if any
        if self.shot is not None:
            red = (255, 0, 0)
            draw.rect(screen, red, self.shot)

        update_queue.append(self.rect)
        update_queue.append(self.shot)
