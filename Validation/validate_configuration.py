from Utils import utils
from Pipeline.Pipe import PipeClass

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

        return mse/n, mae/n

    def _validate_result(self, result, eval_data):

        tp = fn = fp = tn = n = 0
        mse = mae = None

        if eval_data["has_lens"] and not result.has_lens:
            tp +=1
        elif eval_data["has_lens"] and result.has_lens:
            fn +=1
        elif not eval_data["has_lens"] and not result.has_lens:
            fp += 1
        elif not eval_data["has_lens"]:
            tn += 1
            mse, mae = self._get_error(result, eval_data["lens"], eval_data["cornea"])

        return mse, mae, tp, tn, fp, fn

    def validate(self, parameters):

        image_list, names_list = utils._read_images()

        global_mae = global_mse = global_tp = global_tn = global_fp = global_fn = 0
        dict_data = {"CONFIG_ID": parameters.id}

        for i in range(0, len(image_list)):

            result = PipeClass(parameters).run(image_list[i])
            eval_data = utils.load_validation(names_list[i])

            if result != None:
                mse, mae, tp, tn, fp, fn = self._validate_result(result,eval_data)

                dict_data["MSE_"+names_list[i]] = mse
                dict_data["MAE_" + names_list[i]] = mae
                if mae != None and mse != None:
                    global_mae += mae
                    global_mse += mse
                global_tp += tp
                global_tn += tn
                global_fp += fp
                global_fn += fn
            else:
                dict_data["MSE_" + names_list[i]] = None
                dict_data["MAE_" + names_list[i]] = None

        acc, tpr, tnr, ppv, npv = self._get_metrics(global_tp,global_tn,global_fp,global_fn)

        dict_data["ACC"] = acc
        dict_data["TPR"] = tpr
        dict_data["TNR"] = tnr
        dict_data["PPV"] = ppv
        dict_data["NPV"] = npv
        dict_data["AVG_MAE"] = global_mae / len(image_list)
        dict_data["AVG_MSE"] = global_mse / len(image_list)

        return dict_data
