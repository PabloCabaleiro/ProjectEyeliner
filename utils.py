import glob
import cv2

IMG_PATH = "imgenestfm\*.jpeg"

def _read_images():
    image_list = []
    names_list = []
    for filename in glob.glob(IMG_PATH):  # assuming gif
        im = cv2.imread(filename)
        image_list.append(im)
        names_list.append(filename)

    return image_list, names_list