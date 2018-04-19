import glob
import cv2

VAL_PATH = "validation-data\\"
IMG_PATH = "imgenestfm\\*"

def _read_images():
    image_list = []
    names_list = []
    for filename in glob.glob(IMG_PATH):  # assuming gif
        im = cv2.imread(filename)
        image_list.append(im)
        names_list.append(filename)

    return image_list, names_list

def load_validation(name):

    edge = "s"

    sup_l = []
    inf_l = []

    for line in open(VAL_PATH + name.split("\\")[1].split(".")[0] + '.txt', 'r'):
        if line.startswith("NO_LENS"):
            return {"lens": [], "cornea": [], "has_lens": True}
        if line.startswith("MARK"):
            edge = "i"
        elif edge == "s":
            sup_l.append((int(line.split("\t")[0]),int(line.split("\t")[1])))
        else:
            inf_l.append((int(line.split("\t")[0]), int(line.split("\t")[1])))

    return {"lens": sup_l, "cornea": inf_l, "has_lens": False}

def show_validations(list_names, list_images):
    for i in range(0,len(list_names)):
        eval_result = load_validation(list_names[i])
        if not eval_result["has_lens"]:
            image = list_images[i]
            for i in range(1, len(eval_result["cornea"])):
                cv2.line(image, eval_result["cornea"][i - 1], eval_result["cornea"][i], (0, 255, 0))
            for i in range(1, len(eval_result["lens"])):
                cv2.line(image, eval_result["lens"][i - 1], eval_result["lens"][i], (255, 255, 0))
            cv2.imshow("aoi_window", image)
            cv2.waitKey()