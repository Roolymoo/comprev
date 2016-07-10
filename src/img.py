import os.path
from pygame import image


def load_img(img_n):
    '''(str) -> Surface
    Loads img given by img_n and returns as Surface. Assumes img_n valid.'''
    img_folder = "art"
    return image.load(os.path.join(img_folder, img_n))