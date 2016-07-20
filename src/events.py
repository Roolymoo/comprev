from collections import deque
import os.path

from monsters import *


def _get_dict():
    """used for parsing spawner files."""
    return {"type": None, "img": None, "x": None, "y": None, "w": None, "h": None, "fps": None, "path": None}


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


class Spawner:
    """collection of monsters to spawn"""
    def __init__(self):
        self.monsters = deque()
        self.is_spawned = False

    def spawn(self, monster_list, screen, update_queue):
        """appends all monsters to monster_list and renders them"""
        for monster in self.monsters:
            monster_list.append(monster)
            monster.render(screen, update_queue)

        self.is_spawned = True

    def add(self, monster):
        self.monsters.append(monster)

    def remove(self, monster):
        self.monsters.remove(monster)

    def contains(self, monster):
        return monster in self.monsters

    def load(self, file_n, tile_size):
        with open(os.path.join("levels", file_n)) as file:
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

                if data["type"] == "cbot":
                    monster = CaptureBot(tile_size * int(data["x"]), tile_size * int(data["y"]), tile_size * int(data["w"]),
                                     tile_size * int(data["h"]))
                    self.add(monster)
                elif data["type"] == "lbot":
                    monster = LaserBot(tile_size * int(data["x"]), tile_size * int(data["y"]), tile_size * int(data["w"]),
                                   tile_size * int(data["h"]))
                    self.add(monster)
                elif data["type"] == "pbot":
                    monster = PatrolBot(tile_size * int(data["x"]), tile_size * int(data["y"]), tile_size * int(data["w"]),
                                    tile_size * int(data["h"]), int(data["fps"]), _parse_path(data["path"], tile_size))
                    self.add(monster)
                elif data["type"] == "wbot":
                    monster = WaitBot(tile_size * int(data["x"]), tile_size * int(data["y"]), tile_size * int(data["w"]),
                                     tile_size * int(data["h"]))
                    self.add(monster)
                elif data["type"] == "plbot":
                    monster = PatrolLaserBot(tile_size * int(data["x"]), tile_size * int(data["y"]), tile_size * int(data["w"]),
                                         tile_size * int(data["h"]),  int(data["fps"]), _parse_path(data["path"], tile_size))
                    self.add(monster)

                if data["img"]:
                    monster.img = load_img(data["img"])

                line = file.readline()

    def is_done(self):
        """returns true if all monsters have spawned and died, false otherwise"""
        return self.spawned and len(self.monsters) == 0
