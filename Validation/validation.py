import cv2
from Pipeline.process import ProccesClass

from Pipeline.preprocess import PreproccessClass
from Utils.utils import _read_images

VAL_PATH = "validation\\"

class ValidateClass(object):

    def _load_validation(self,name):

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

        return sup_l, inf_l, False

    def _show_validations(self, list_names, list_images):
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

        with open(VAL_PATH + name.split("\\")[1].split(".")[0] + '.txt', 'w') as file:
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

        image_list, names_list = _read_images()

        self._set_validation_points(image_list,names_list)

    def validate(self):

        image_list, names_list = _read_images()
        tp = tn = fp = fn = mse = mae = n = 0

        for i in range(0, len(image_list)):
            top_line, bot_line, no_lens = self._load_validation(names_list[i])
            rotated_img, rotation_matrix = PreproccessClass(image_list[i]).pipeline()
            predicted_top_line, predicted_bot_line, n_capas = ProccessClass(rotated_img).pipeline()

            if no_lens and n_capas < 3:
                tp +=1
            elif no_lens and n_capas == 3:
                fn +=1
            elif not no_lens and n_capas < 3:
                fp += 1
            elif not no_lens:
                tn += 1
                mse_img, mae_img, n_img = self._get_error(predicted_top_line,predicted_bot_line,top_line,bot_line)
                mse += mse_img
                mae += mae_img
                n += n_img

        mse = mse/n
        acc, tpr, tnr, ppv, npv = self._get_metrics(tp,tn,fp,fn)

        return {mse: mse, acc: acc, tpr: tpr, tnr: tnr, ppv: ppv, npv: npv}

    def _get_metrics(self, tp, tn, fp, fn):
        tpr = tp / (tp + fn) # sensitivity or true positive rate
        tnr = tn / (tn + fp) # specifity or true negative rate
        ppv = tp / (tp + fp) # precision or positive predictive value
        npv = tn / (tn + fn) # negative preditive value
        acc = (tp + tn) / (tp + tn + fp + fn) # accuracy
        return acc, tpr, tnr, ppv, npv

    def _get_error(self, result, top_line, bot_line):
        # Return Mean Square Error and Mean Absolute Error
        mse = mae = 0
        n = len(top_line) + len(bot_line)

        for x,y in top_line:
            pred = result.get_lens_pos(x)
            if pred > -1:
                res = y - pred
                mse += (res)**2
                mae += abs(res)

        for x,y in bot_line:
            pred = result.get_cornea_pos(x)
            if pred > 1:
                res = y - pred
                mse += (res)**2
                mae += abs(res)

        return mse, mae, n
