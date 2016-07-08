from pygame import Rect

from obj import Obj


def is_clicked(object, pos):
    """(*, tuple) -> bool
    Returns True if POS is contained in object.rect, otherwise False."""
    # Note colliderect will not return True if pos is on the bottom or right edge
    return object.rect.collidepoint(pos)


def is_collides(rect, *args):
    for obj_list in args:
        for obj in obj_list:
            if obj is Rect and rect.colliderect(obj):
                return True
            elif rect.colliderect(obj.rect):
                return True

    return False
