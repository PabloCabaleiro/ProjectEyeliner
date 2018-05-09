import cv2
from Utils import utils
import os.path


class ValidateData(object):

    path = None

    def __init__(self):
        self.path = utils.VAL_PATH

    def _set_validation_points(self, images_list, names_list):

        for i in range(0,len(images_list)):

            if not os.path.isfile(utils.VAL_PATH + names_list[i].split("\\")[1].split(".")[0] + '.txt'):
                self._create_contour_validation(images_list[i],names_list[i])

    def load_image(self, name, image, aoi_params):

        image = image * 1

        font = cv2.FONT_HERSHEY_PLAIN
        if aoi_params["line"] == "S":
            cv2.putText(image, 'Press space to change line', (10, 20), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(image, 'Press space to save image', (10, 20), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, 'Press D to delete the last point', (10, 40), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, 'Press 2 to mark image with no lens', (10, 60), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        l_sup = list(aoi_params["points_s"])
        for i in range(1, len(l_sup)):
            cv2.line(image, l_sup[i - 1], l_sup[i], (255, 255, 0))

        if aoi_params["line"] == "i":
            l_inf = list(aoi_params["points_i"])
            for i in range(1, len(l_inf)):
                cv2.line(image, l_inf[i - 1], l_inf[i], (0, 255, 0))

        cv2.imshow(name, image)

    def _create_contour_validation(self, image, name):
        aoi_params = dict(line = 's', points_s=[], points_i = [], image=image, name= name)

        cv2.namedWindow(name)
        cv2.moveWindow(name, 40,30)
        cv2.setMouseCallback(name, self._on_mouse_clicked_aoi, aoi_params)
        stop = False
        no_lens = False

        while not stop:

            self.load_image(name, image, aoi_params)
            k = cv2.waitKey() & 0xff

            if (k == ord('\n') or k == ord(' ')) and aoi_params["line"]=='s':
                aoi_params["line"] = 'i'
                list(aoi_params["points_s"])

            elif k == ord('\n') or k == ord(' '):
                stop = True

            elif k == ord("d") or k == ord("D"):
                aoi_params["points_"+aoi_params["line"]] = aoi_params["points_"+aoi_params["line"]][:-1]

            elif k == ord("2"):
                no_lens = True
                stop = True

        cv2.destroyWindow(name)
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

        self.load_image(aoi_params["name"], img_copy, aoi_params)

    def create_validation(self):

        image_list, names_list = utils._read_images()
        self._set_validation_points(image_list,names_list)


