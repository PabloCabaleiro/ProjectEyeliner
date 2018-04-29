import glob
import cv2
import math
import matplotlib.pyplot as plt

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

def get_dist(point1,point2):
    return math.sqrt((point2[1]-point1[1])**2 + (point2[0]-point1[0])**2)

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

def distances_to_color(distances):
    max_dist = max(distances)
    min_dist = min(distances)
    colors = []
    norm_dist = [(value-min_dist)/(max_dist-min_dist) for value in distances]
    for value in norm_dist:
        if value > 0.9:
            colors.append((0, 255, 0))
        elif value > 0.8:
            colors.append((102, 255, 51))
        elif value > 0.7:
            colors.append((153, 255, 51))
        elif value > 0.6:
            colors.append((204, 255, 51))
        elif value > 0.5:
            colors.append(((255, 255, 0)))
        elif value > 0.4:
            colors.append((255, 204, 0))
        elif value > 0.3:
            colors.append((255, 153, 51))
        elif value > 0.2:
            colors.append((255, 102, 0))
        elif value > 0.1:
            colors.append((255, 51, 0))
        elif value > 0:
            colors.append((255, 0, 0))

def onclick(self, event):
    x = event.x
    y = event.y

    #Check top line
    top_x = x - self.top2bot["start"]
    top_point = self.top2bot["line"][top_x]
    if (x,y) == top_point:
        plt.plot([x,top_point[0]],[y,top_point[1]])

    #Check bot line
    bot_x = x - self.bot2top["start"]
    bot_point = self.bot2top["line"][bot_x]
    if (x, y) == bot_point:
        plt.plot([x, bot_point[0]], [y, bot_point[1]])


def show_metrics(self, image):
    fig, ax = plt.figure("Vertical metric")
    plt.imshow(image)
    colors = distances_to_color(self.top2bot["distances"])

    for i in range(0,len(self.top2bot["distances"])):
        point = self.top2bot["line"][i]
        plt.plt(point[0],point[1], color = colors[i])
    colors = distances_to_color(self.bot2top["distances"])

    for i in range(0,len(self.bot2top["distances"])):
        point = self.bot2top["line"][i]
        plt.plt(point[0],point[1], color = colors[i])

    cid = fig.canvas.mpl_connect('button_press_event', lambda event: onclick(self, event))