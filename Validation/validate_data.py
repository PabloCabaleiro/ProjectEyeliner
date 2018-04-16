import cv2
from Utils import utils

class ValidateData(object):

    path = None

    def __init__(self):
        self.path = utils.VAL_PATH

    def _set_validation_points(self, images_list, names_list):

        for i in range(0,len(images_list)):
            self._create_contour_validation(images_list[i],names_list[i])

    def _create_contour_validation(self, image, name):
        aoi_params = dict(line = 's', points_s=[], points_i = [], image=image)

        cv2.namedWindow("aoi_window")
        cv2.setMouseCallback("aoi_window", self._on_mouse_clicked_aoi, aoi_params)
        stop = False
        no_lens = False

        while not stop:
            cv2.imshow("aoi_window", image)
            k = cv2.waitKey() & 0xff
            if (k == ord('\n') or k == ord(' ')) and aoi_params["line"]=='s':
                aoi_params["line"] = 'i'
                l_sup = list(aoi_params["points_s"])
                for i in range(1, len(l_sup)):
                    cv2.line(image, l_sup[i - 1], l_sup[i], (255, 255, 0))
            elif k == ord('\n') or k == ord(' '):
                stop = True
            elif k == ord("d") or k == ord("D"):

                if len(list(aoi_params["points_"+aoi_params["line"]]))>0:
                    aoi_params["points_"+aoi_params["line"]] = aoi_params["points_"+aoi_params["line"]][:-1]

                l_sup = list(aoi_params["points_s"])
                for i in range(1, len(l_sup)):
                    cv2.line(image, l_sup[i - 1], l_sup[i], (255, 255, 0))

                if aoi_params["line"] == "i":
                    l_inf = list(aoi_params["points_i"])
                    for i in range(1, len(l_inf)):
                        cv2.line(image, l_inf[i - 1], l_inf[i], (0, 255, 0))

            elif k == ord("2"):
                no_lens = True
                stop = True

        s_list = list(aoi_params["points_s"])
        i_list = list(aoi_params["points_i"])

        if not no_lens:
            output  = ""
            for x,y in s_list:
                output += str(x) + "\t" + str(y) + "\n"
            output += "MARK\n"
            for x,y in i_list:
                output += str(x) + "\t" + str(y) + "\n"
        else:
            output = "NO_LENS"

        with open(self.path + name.split("\\")[1].split(".")[0] + '.txt', 'w') as file:
            file.write(output)
            file.close()

    def _on_mouse_clicked_aoi(self, event, x, y, flags, aoi_params):

        img_copy = aoi_params["image"] * 1

        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(img_copy, (x, y), 3, (0, 255, 255), 2)

        elif event == cv2.EVENT_LBUTTONUP:
            l = list(aoi_params["points_"+aoi_params["line"]])
            l.append((x, y))
            aoi_params["points_"+aoi_params["line"]] = l

        l_inf = list(aoi_params["points_i"])
        for i in range(1, len(l_inf)):
            cv2.line(img_copy, l_inf[i - 1], l_inf[i], (0, 255, 0))

        l_sup = list(aoi_params["points_s"])
        for i in range(1,len(l_sup)):
            cv2.line(img_copy, l_sup[i-1], l_sup[i], (255, 255, 0))

        cv2 .imshow("aoi_window", img_copy)

    def create_validation(self):

        image_list, names_list = utils._read_images()

        self._set_validation_points(image_list,names_list)


