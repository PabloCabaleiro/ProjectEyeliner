import glob
import cv2
import math
import matplotlib.pyplot as plt
import numpy as np

VAL_PATH = "validation-data\\"
IMG_PATH = "imgenestfm\\*"
PROBLEMS_PATH = "problemas\\*"


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
    clean_distances = [i for i in distances if i> -1]
    max_dist = max(distances)
    min_dist = min(clean_distances)
    colors = []
    mean_dist = np.mean(clean_distances)
    dist_range = (max_dist - min_dist)
    norm_dist = []

    for i in range(0, len(distances)):
        if distances[i] == -1:
            norm_dist.append(mean_dist)
        else:
            norm_dist.append((distances[i]-min_dist)/dist_range)

    for i in range(0,len(norm_dist)):
        if distances[i] == -1:
            colors.append((0,0,0))
        elif norm_dist[i] > 0.9:
            colors.append((0, 255, 0))
        elif norm_dist[i] > 0.8:
            colors.append((50, 255, 100))
        elif norm_dist[i] > 0.7:
            colors.append((50, 255, 150))
        elif norm_dist[i] > 0.6:
            colors.append((50, 255, 200))
        elif norm_dist[i] > 0.5:
            colors.append(((0, 255, 255)))
        elif norm_dist[i] > 0.4:
            colors.append((0, 200, 255))
        elif norm_dist[i] > 0.3:
            colors.append((50, 150, 255))
        elif norm_dist[i] > 0.2:
            colors.append((0, 100, 255))
        elif norm_dist[i] > 0.1:
            colors.append((0, 50, 255))
        elif norm_dist[i] >= 0:
            colors.append((0, 0, 255))
    return colors


def show_metrics(self, image, name):

    top2bot_colors = distances_to_color(self.top2bot["distances"])
    bot2top_colors = distances_to_color(self.bot2top["distances"])

    aoi_params = dict(top2bot_line = self.top2bot["line"], top2bot_points = self.top2bot["points"],  top2bot_start = self.top2bot["start"], top2bot_end = self.top2bot["end"], top2bot_dist = self.top2bot["distances"],
                      bot2top_line = self.bot2top["line"], bot2top_points = self.bot2top["points"], bot2top_start = self.bot2top["start"], bot2top_end = self.bot2top["end"], bot2top_dist = self.bot2top["distances"],
                      image=image, name = name)

    for i in range(1, len(self.top2bot["distances"])):
        point = self.top2bot["line"][i]
        image[point[1]-2, point[0], :] = top2bot_colors[i]
        image[point[1]-1, point[0], :] = top2bot_colors[i]
        image[point[1],point[0],:] = top2bot_colors[i]
        image[point[1]+1, point[0], :] = top2bot_colors[i]
        image[point[1]+2, point[0], :] = top2bot_colors[i]

    for i in range(1, len(self.bot2top["distances"])):
        point = self.bot2top["line"][i]
        image[point[1]-2, point[0], :] = bot2top_colors[i]
        image[point[1]-1, point[0], :] = bot2top_colors[i]
        image[point[1],point[0],:] = bot2top_colors[i]
        image[point[1]+1, point[0], :] = bot2top_colors[i]
        image[point[1]+2, point[0], :] = bot2top_colors[i]


    cv2.namedWindow(name)
    cv2.setMouseCallback(name, _on_mouse_clicked_aoi, aoi_params)
    cv2.imshow(name, image)
    cv2.waitKey()
    cv2.destroyAllWindows()



def _on_mouse_clicked_aoi(event, x, y, flags, aoi_params):

    img_copy = aoi_params["image"] * 1

    if event == cv2.EVENT_LBUTTONDOWN:
        if x >= aoi_params["top2bot_start"] and x <= aoi_params["top2bot_end"]:
            pos = int(x - aoi_params["top2bot_start"])
            if y-5 < aoi_params["top2bot_line"][pos][1] < y+5:
                cv2.line(img_copy, aoi_params["top2bot_line"][pos], aoi_params["top2bot_points"][pos], (255,255,0))
                print_text(img_copy,str(aoi_params["top2bot_dist"][pos]))
                cv2.imshow(aoi_params["name"], img_copy)
        if x >= aoi_params["bot2top_start"] and x <=aoi_params["bot2top_end"]:
            pos = int(x - aoi_params["bot2top_start"])
            if y-5 < aoi_params["bot2top_line"][pos][1] < y+5:
                cv2.line(img_copy, aoi_params["bot2top_line"][pos], aoi_params["bot2top_points"][pos],(255,255,0))
                print_text(img_copy,str(aoi_params["bot2top_dist"][pos]))
                cv2.imshow(aoi_params["name"], img_copy)


def fpoints2ipoints(top_line_inv, bot_line_inv):

    top_line_result = []
    start_index = int(top_line_inv[0][0])
    current_index = start_index
    for i in range(0,len(top_line_inv)):
        point_index = int(top_line_inv[i][0])
        if point_index == current_index:
            top_line_result.append((current_index,int(top_line_inv[i][1])))
            current_index += 1
        elif point_index > current_index:
            top_line_result.append((current_index, int((top_line_inv[i-1][1] + top_line_inv[i][1])/2)))
            current_index += 1


    bot_line_result = []
    start_index = int(bot_line_inv[0][0])
    current_index = start_index
    for i in range(0, len(bot_line_inv)):
        point_index = int(bot_line_inv[i][0])
        if point_index == current_index:
            bot_line_result.append((current_index, int(bot_line_inv[i][1])))
            current_index += 1
        elif point_index > current_index:
            bot_line_result.append((current_index, int((bot_line_inv[i - 1][1] + bot_line_inv[i][1]) / 2)))
            current_index += 1

    return top_line_result, bot_line_result

def print_text(image, text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (30, 30)
    fontScale = 1
    fontColor = (255, 255, 255)
    lineType = 2

    cv2.putText(image, text,
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)