from collections import deque


def load_level(level):
    """"Returns env_obj_list, monster_list."""
    env_obj_list = deque()
    monster_list = deque()
    with open(level) as file:
        line = file.readline()
        while line:
            data = dict()
            for raw_data in line.split():
                id, val = raw_data.split("=")
                data.update({id: val})
