from collections import deque
import os.path

from pygame import transform, Rect, font

from obj import Obj, Portal
from monsters import CaptureBot, LaserBot, PatrolBot, WaitBot, PatrolLaserBot
from img import load_img
from player import Player
from events import Spawner


def _get_dict():
    """Used for parsing levels."""
    return {"type": None, "img": None, "x": None, "y": None, "w": None, "h": None, "flip": None, "rotate": None,
            "scale": None, "fps": None, "file": None, "path": None}


def _parse_path(path_raw, tile_size):
    path = dict()
    i = 0
    for rect_raw in path_raw.strip("[]").split("."):
        _rect_raw = rect_raw.strip("()").split(",")
        x, y, w, h = [tile_size * int(x) for x in _rect_raw[:-1]]
        t = int(_rect_raw[-1])
        if _rect_raw:
            path.update({i: [Rect(x, y, w, h), t]})
            i += 1

    return path


def load_level(level, tile_size, window_width, window_height, background, screen, update_queue):
    """Categorizes all items in level as env_obj's, monsters, player, or portal. Initializes them and renders them. Returns
    player, portal, env_obj_list, monster_list. Levels are permitted to have lines beginning with # to indicate a comment which
    will be ignored."""
    env_obj_list = deque()
    monster_list = deque()
    event_list = deque()
    portal = None
    player = None
    with open(level) as file:
        line = file.readline()
        while line:
            if line[0] == "#":
                # comment
                line = file.readline()
                continue

            data = _get_dict()
            for raw_data in line.split():
                id, val = raw_data.split("=")
                data.update({id: val})

            if data["type"] == "obj":
                obj = Obj(tile_size * int(data["x"]), tile_size * int(data["y"]), tile_size * int(data["w"]),
                          tile_size * int(data["h"]))
                env_obj_list.append(obj)
            elif data["type"] == "cbot":
                obj = CaptureBot(tile_size * int(data["x"]), tile_size * int(data["y"]), tile_size * int(data["w"]),
                                 tile_size * int(data["h"]))
                monster_list.append(obj)
            elif data["type"] == "lbot":
                obj = LaserBot(tile_size * int(data["x"]), tile_size * int(data["y"]), tile_size * int(data["w"]),
                               tile_size * int(data["h"]))
                monster_list.append(obj)
            elif data["type"] == "pbot":
                obj = PatrolBot(tile_size * int(data["x"]), tile_size * int(data["y"]), tile_size * int(data["w"]),
                                tile_size * int(data["h"]), int(data["fps"]), _parse_path(data["path"], tile_size))
                monster_list.append(obj)
            elif data["type"] == "wbot":
                obj = WaitBot(tile_size * int(data["x"]), tile_size * int(data["y"]), tile_size * int(data["w"]),
                              tile_size * int(data["h"]))
                monster_list.append(obj)
            elif data["type"] == "plbot":
                obj = PatrolLaserBot(tile_size * int(data["x"]), tile_size * int(data["y"]), tile_size * int(data["w"]),
                                     tile_size * int(data["h"]),  int(data["fps"]), _parse_path(data["path"], tile_size))
                monster_list.append(obj)
            elif data["type"] == "player":
                obj = Player(tile_size * int(data["x"]), tile_size * int(data["y"]), tile_size * int(data["w"]),
                             tile_size * int(data["h"]), window_width, window_height)
                player = obj
            elif data["type"] == "portal":
                obj = Portal(tile_size * int(data["x"]), tile_size * int(data["y"]), tile_size * int(data["w"]),
                             tile_size * int(data["h"]))
                background.obj_list.append(obj)
                portal = obj
            elif data["type"] == "bkgrd":
                obj = Obj(tile_size * int(data["x"]), tile_size * int(data["y"]), tile_size * int(data["w"]),
                          tile_size * int(data["h"]))
                background.obj_list.append(obj)
            elif data["type"] == "txt":
                obj = Obj(tile_size * int(data["x"]), tile_size * int(data["y"]), tile_size * int(data["w"]),
                          tile_size * int(data["h"]))
                text = data["txt"].replace("^", " ")
                obj.img = font.Font(os.path.join("fonts", "data-latin.ttf"), int(0.7 * tile_size * int(data["h"]))).render(text, True, (0, 0, 0))
                background.obj_list.append(obj)
            elif data["type"] == "spwn":
                obj = Spawner()
                obj.load(data["file"], tile_size)
                event_list.append(obj)


            if data["img"]:
                obj.img = load_img(data["img"])
            if data["flip"]:
                horiz, vert = None, None
                args = data["flip"].strip("()").split(",")
                if args[0] == "false":
                    horiz = False
                else:
                    horiz = True
                if args[1] == "false":
                    vert = False
                else:
                    vert = True

                obj.img = transform.flip(obj.img, horiz, vert)
            if data["rotate"]:
                obj.img = transform.rotate(obj.img, int(data["rotate"].split("=")[-1]))
            if data["scale"]:
                obj.img = transform.scale(obj.img, tuple(tile_size * int(i) for i in data["scale"].strip("()").split(",")))

            if data["img"] and obj.img:
                obj.render(screen, update_queue)

            line = file.readline()

    return player, portal, env_obj_list, monster_list, event_list
