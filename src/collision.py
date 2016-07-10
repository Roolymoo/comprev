from pygame import Rect

from obj import Obj


# def is_clicked(object, pos):
#     """(*, tuple) -> bool
#     Returns True if POS is contained in object.rect, otherwise False."""
#     # Note colliderect will not return True if pos is on the bottom or right edge
#     return object.rect.collidepoint(pos)


def is_collides(rect, *args):
    """args is a collection of iterables each containing objects. Returns object rect collides
    with if that occurs, otherwise returns None."""
    for obj_col in args:
        for obj in obj_col:
            if isinstance(obj, Rect) and rect.colliderect(obj):
                return obj
            elif rect.colliderect(obj.rect):
                return obj

    return None


# def is_adjacent(rect1, rect2):
#     """Returns True if rect1 and rect2 share a side (e.g. bottom line of rect1 overlaps with
#     top line of rect2), otherwise False. (colliderect doesn't check for this.)"""
#     rect1_c = rect1.copy()
#
#     rect1_c.x += 1
#     if rect1_c.colliderect(rect2):
#         return True
#
#     rect1_c.x -= 2
#     if rect1_c.colliderect(rect2):
#         return True
#
#     rect1_c.x += 1
#     rect1_c.y += 1
#     if rect1_c.colliderect(rect2):
#         return True
#
#     rect1_c.y -= 2
#     if rect1_c.colliderect(rect2):
#         return True
#
#     return False
