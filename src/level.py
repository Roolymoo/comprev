from collections import deque

from pygame import transform

from obj import Obj
from monsters import CaptureBot, LaserBot
from img import load_img
from player import Player


def _get_dict():
    """Used for parsing levels."""
    return {"type": None, "img": None, "x": None, "y": None, "w": None, "h": None, "flip": None, "rotate": None}


def load_level(level, tile_size, window_width, window_height, screen, update_queue):
    """Categorizes all items in level as env_obj's, monsters, player, or portal. Initializes them and renders them. Returns
    player, portal, env_obj_list, monster_list. Levels are permitted to have lines beginning with # to indicate a comment which
    will be ignored."""
    env_obj_list = deque()
    monster_list = deque()
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
            elif data["type"] == "player":
                obj = Player(tile_size * int(data["x"]), tile_size * int(data["y"]), tile_size * int(data["w"]),
                             tile_size * int(data["h"]), window_width, window_height)
                player = obj
            elif data["type"] == "portal":
                obj = Obj(tile_size * int(data["x"]), tile_size * int(data["y"]), tile_size * int(data["w"]),
                          tile_size * int(data["h"]))
                portal = obj

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

            if obj.img:
                obj.render(screen, update_queue)

            line = file.readline()

    return player, portal, env_obj_list, monster_list
