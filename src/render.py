from pygame import display

import collision
from background import Background


def update_display(update_queue):
    """(deque) -> NoneType
    Updates display with Rects given in update_queue, and clears update_queue."""
    display.update(update_queue)

    update_queue.clear()


# def clear(screen, obj_list, obj, update_queue):
#     """(Surface, list, *, deque) -> NoneType
#     For each obj in obj_list that obj overlaps with, call their render() method."""
#     for elem in obj_list:
#         if collision.is_collides(elem, obj):
#             if elem is Background:
#                 elem.render(screen, update_queue, obj.rect)
#             else:
#                 elem.render(screen, update_queue)
