import os.path
from pygame import image

def load_sizes(size_file):
    '''str -> None
    Returns a dictionary containing sizes of objects, loading from the given
    file size_file.
    '''
    img_folder = "art"

    size = dict()

    # Open the sizes file and load image sizes into size
    f = open(os.path.join(img_folder, size_file), 'r')
    for line in f.readlines():
        if line != "":
            img_info = line.split()
            size[img_info[0]] = (int(img_info[1]), int(img_info[2]))

    f.close()

    return size

def load_img(img_n):
    '''(str) -> Surface
    Loads img given by img_n and returns as Surface. Assumes img_n valid.'''
    img_folder = "art"
    return image.load(os.path.join(img_folder, img_n))