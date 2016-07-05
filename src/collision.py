##############################################################################
#
# Methods for collision detection.
#
##############################################################################


def is_clicked(object, pos):
    """(*, tuple) -> bool
    Returns True if POS is contained in object.rect, otherwise False."""
    # Note colliderect will not return True if pos is on the bottom or right edge
    return object.rect.collidepoint(pos)


def is_collides(object1, object2):
    """(*, *) -> bool
    Returns true if the .rect attributes of each object collide. Note that only intersection of top and bottom, or left
    and right edges returns false."""
    return object1.rect.colliderect(object2.rect)
