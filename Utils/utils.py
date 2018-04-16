import glob
import cv2

VAL_PATH = "validation-data\\"
IMG_PATH = "imgenestfm\*.jpeg"

def _read_images():
    image_list = []
    names_list = []
    for filename in glob.glob(IMG_PATH):  # assuming gif
        im = cv2.imread(filename)
        image_list.append(im)
        names_list.append(filename)

    return image_list, names_list

def load_validation(self,name):

    edge = "s"

    sup_l = []
    inf_l = []

    for line in open(VAL_PATH + name.split("\\")[1].split(".")[0] + '.txt', 'r'):
        if line.startswith("NO_LENS"):
            return [],[],True
        if line.startswith("MARK"):
            edge = "i"
        elif edge == "s":
            sup_l.append((int(line.split("\t")[0]),int(line.split("\t")[1])))
        else:
            inf_l.append((int(line.split("\t")[0]), int(line.split("\t")[1])))

    return {"lens": sup_l, "cornea": inf_l, "has_lens": False}

def show_validations(self, list_names, list_images):
    for i in range(0,len(list_names)):
        inf_l, sup_l, has_lens  = self._load_validation(list_names[i])
        if not has_lens:
            image = list_images[i]
            for i in range(1, len(inf_l)):
                cv2.line(image, inf_l[i - 1], inf_l[i], (0, 255, 0))
            for i in range(1, len(sup_l)):
                cv2.line(image, sup_l[i - 1], sup_l[i], (255, 255, 0))
            cv2.imshow("aoi_window", image)
            cv2.waitKey()