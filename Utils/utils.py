import glob
import cv2
import math

IMG_PATH = "imgenestfm\*.jpeg"

def _read_images():
    image_list = []
    names_list = []
    for filename in glob.glob(IMG_PATH):  # assuming gif
        im = cv2.imread(filename)
        image_list.append(im)
        names_list.append(filename)

    return image_list, names_list

def get_dist(self,point1,point2):
    return math.sqrt((point2[1]-point1[1])**2 + (point2[0]-point1[1])**2)