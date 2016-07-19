import os.path

from pygame import Rect, draw, mixer, time

from collision import is_collides
from img import load_img


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


def _is_in_sight(wbot, player, *args):
    b_x, b_y, b_w, b_h = wbot.rect
    bond_x = player.bond_x + player.rect.w
    bond_y = player.bond_y + player.rect.h

    # rect's emanating from wbot in all directions to border of screen
    left_rect = Rect(0, b_y, b_x, b_h)
    right_rect = Rect(b_x + b_w, b_y, bond_x - (b_x + b_w), b_h)
    up_rect = Rect(b_x, 0, b_w, b_y)
    down_rect = Rect(b_x, b_y + b_h, b_w, bond_y - (b_y + b_h))

    # see if any of these rect's intersect with player without colliding with anything in-between
    for rect in (left_rect, right_rect, up_rect, down_rect):
        if rect.colliderect(player.rect):
            # hit player, modify rect to extend only to player
            p_x, p_y, p_w, p_h = player.rect
            if rect == left_rect:
                rect.x = p_x + p_w
                rect.w -= p_x + p_w
            elif rect == right_rect:
                rect.w -= bond_x - p_x
            elif rect == up_rect:
                rect.y = p_y + p_h
                rect.h -= p_y + p_h
            elif rect == down_rect:
                rect.h -= bond_y - p_y

            if is_collides(rect, *args):
                # obstacles in way, no good (player shouldn't be in args)
                continue
            else:
                # player visible
                return True

    return False


def _is_clear_shot(lbot, dir, player, *args):
    """Checks if there is no obstruction between lbot and player. If there isn't, a rect is
    loaded into lbot.shot for shooting phase, and True is returned. Otherwise False is
    returned."""
    # create rectangle extending from middle of lbot to edge of screen
    lb_x, lb_y, lb_w, lb_h = lbot.rect
    incr_w = int(lb_w / 3)
    incr_h = int(lb_h / 3)
    bond_x = player.bond_x + player.rect.w
    bond_y = player.bond_y + player.rect.h
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


def _patrol(pbot, *args):
    p_x = pbot.path[pbot.i][0].x
    p_y = pbot.path[pbot.i][0].y
    b_x = pbot.rect.x
    b_y = pbot.rect.y

    if p_x < b_x:
        _move(pbot, "left", *args)
    if p_x > b_x:
        _move(pbot, "right", *args)
    if p_y < b_y:
        _move(pbot, "up", *args)
    if p_y > b_y:
        _move(pbot, "down", *args)

    if pbot.rect == pbot.path[pbot.i][0]:
        # reached node in path
        if pbot.path[pbot.i][1] != 0:
            # wait at this node in path
            pbot.clock = time.Clock()
        else:
            pbot.advance()


class BotMess:
    def __init__(self, rect):
        self.rect = rect
        self.img = load_img("remains.png")

    def render(self, screen, update_queue):
        screen.blit(self.img, self.rect)

        update_queue.append(self.rect)


class CaptureBot:
    """Tries to contact (capture) player (be in within 0 pixels in some direction from player)."""

    def __init__(self, x, y, w, h):
        self.rect = Rect(x, y, w, h)
        self.img = None
        self.noise = mixer.Sound(os.path.join("sounds", "explosion_hard1.wav"))
        self.mov_unit = int(w / 25)
        # Most recently collided into object
        self.adj_obj = None

    def move(self, player, *args):
        """args is a collection of iterables each containing objects. Moves closer to rect (for Capture bot it is Player)."""
        p_x = player.rect.x
        p_y = player.rect.y
        b_x = self.rect.x
        b_y = self.rect.y

        if p_x < b_x:
            _move(self, "left", [player], *args)
        if p_x > b_x:
            _move(self, "right", [player], *args)
        if p_y < b_y:
            _move(self, "up", [player], *args)
        if p_y > b_y:
            _move(self, "down", [player], *args)

        # doesn't move if it can't get closer to player

    def render(self, screen, update_queue):
        screen.blit(self.img, self.rect)

        update_queue.append(self.rect)

    def on_death(self):
        self.noise.play()

        return BotMess(self.rect.copy())


class WaitBot(CaptureBot):
    """A capture bot that waits until player is in line of sight, then functions just as a capture bot."""
    def __init__(self, x, y, w, h):
        CaptureBot.__init__(self, x, y, w, h)
        # whether bot has seen player or not
        self.sighted = False

    def move(self, player, *args):
        if not self.sighted:
            if _is_in_sight(self, player, *args):
                self.sighted = True
            else:
                return

        CaptureBot.move(self, player, *args)


class LaserBot(CaptureBot):
    def __init__(self, x, y, w, h):
        CaptureBot.__init__(self, x, y, w, h)
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


class PatrolBot(WaitBot):
    def __init__(self, x, y, w, h, fps, path):
        WaitBot.__init__(self, x, y, w, h)
        # path always starts with self's rect
        self.path = path
        # current rect in path heading to
        self.i = 0
        # for waiting at nodes in path
        self.time = 0
        self.clock = None
        self.fps = fps

    def advance(self):
        """advance node in path."""
        self.i = (self.i + 1) % len(self.path)

    def move(self, player, *args):
        """loops path if not sighted player, otherwise chases player."""
        if not self.sighted:
            if _is_in_sight(self, player, *args):
                self.sighted = True
            elif self.clock:
                # waiting at a node in path
                self.time += self.clock.tick(self.fps)
                if self.time >= self.path[self.i][1]:
                    # ready move to next node
                    self.clock = None
                    self.time = 0
                return
            else:
                _patrol(self, *args)
                return

        # sighted player, continue chase
        CaptureBot.move(self, player, *args)


class PatrolLaserBot(PatrolBot, LaserBot):
    def __init__(self, x, y, w, h, fps, rect_list):
        PatrolBot.__init__(self, x, y, w, h, fps, rect_list)
        self.shot = None

    def move(self, player, *args):
        if not self.sighted:
            if _is_in_sight(self, player, *args):
                self.sighted = True
            elif self.clock:
                # waiting at a node in path
                self.time += self.clock.tick(self.fps)
                if self.time >= self.path[self.i][1]:
                    # ready move to next node
                    self.clock = None
                    self.time = 0
                    self.advance()
                return
            else:
                _patrol(self, *args)
                return

        # sighted player, try to zap him!
        LaserBot.move(self, player, *args)

    def render(self, screen, update_queue):
        LaserBot.render(self, screen, update_queue)
