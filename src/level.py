from collections import deque

from pygame import transform

from obj import Obj
from monsters import CaptureBot, LaserBot
from img import load_img


def _get_dict():
    """Used for parsing levels."""
    return {"type": None, "img": None, "x": None, "y": None, "w": None, "h": None, "flip": None, "rotate": None}


def load_level(level, tile_size, screen, update_queue):
    """Categorizes all items in level as env_obj's or monsters. Initializes them and renders them. Returns env_obj_list,
    monster_list. Levels are permitted to have lines beginning with # to indicate a comment which will be ignored."""
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

            obj.render(screen, update_queue)

            line = file.readline()

    return env_obj_list, monster_list
