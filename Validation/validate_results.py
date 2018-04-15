from Pipeline.process import ProccesClass
from Pipeline.preprocess import PreproccessClass
from Utils.utils import _read_images

class ValidateResults(object):

    def validate(self):

        image_list, names_list = _read_images()
        tp = tn = fp = fn = mse = mae = n = 0

        for i in range(0, len(image_list)):
            top_line, bot_line, no_lens = self._load_validation(names_list[i])
            rotated_img, rotation_matrix = PreproccessClass(image_list[i]).pipeline()
            predicted_top_line, predicted_bot_line, n_capas = ProccesClass(rotated_img).pipeline()

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