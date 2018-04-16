from Utils import utils
from Pipeline.process import ProccesClass
from Pipeline.preprocess import PreproccessClass

class ValidateConfiguration(object):

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

    def _validate_result(self, result, eval_data):

        tp = fn = fp = tn = mse = mae = n = 0

        if eval_data.has_lens and result.n_capas < 3:
            tp +=1
        elif eval_data.no_lens and result.n_capas == 3:
            fn +=1
        elif not eval_data.no_lens and result.n_capas < 3:
            fp += 1
        elif not eval_data.no_lens:
            tn += 1
            mse_img, mae_img, n_img = self._get_error(result.lens, result.cornea, eval_data.lens, eval_data.cornea)
            mse += mse_img
            mae += mae_img
            n += n_img

        mse = mse/n
        mae = mae/n

        return mse, mae, tp, tn, fp, fn

    def validate(self, parameters):

        image_list, names_list = utils._read_images()

        preprocces = PreproccessClass(parameters)
        procces = ProccesClass(parameters)

        global_mae = global_mse = global_tp = global_tn = global_fp = global_fn = 0
        dict_data = {"CONFIG_ID": parameters.id}

        for i in range(0, len(image_list)):
            rotated_img, enhanced_image, rotation_matrix = preprocces.pipeline(image_list[i])
            result = procces.pipeline(rotated_img, enhanced_image, rotation_matrix)
            eval_data = utils.load_validation(names_list[i])
            mse, mae, tp, tn, fp, fn = self._validate_result(result,eval_data)

            dict_data["MSE_"+names_list[i]] = mse
            dict_data["MAE_" + names_list[i]] = mae
            global_mae += mae
            global_mse += mse
            global_tp += tp
            global_tn += tn
            global_fp += fp
            global_fn += fn

        acc, tpr, tnr, ppv, npv = self._get_metrics(global_tp,global_tn,global_fp,global_fn)

        dict_data["ACC"] = acc
        dict_data["TPR"] = tpr
        dict_data["TNR"] = tnr
        dict_data["PPV"] = ppv
        dict_data["NPV"] = npv
        dict_data["AVG_MAE"] = global_mae / len(image_list)
        dict_data["AVG_MSE"] = global_mse / len(image_list)

        return dict_data
