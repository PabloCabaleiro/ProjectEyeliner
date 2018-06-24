from Utils import utils
from Pipeline.Pipe import PipeClass
from scipy import stats
from Metrics.metrics import MetricsClass
import numpy as np

class ValidateConfiguration(object):

    def _get_metrics(self, tp, tn, fp, fn):
        tpr = tp / (tp + fn) # sensitivity or true positive rate
        tnr = tn / (tn + fp) # specifity or true negative rate
        ppv = tp / (tp + fp) # precision or positive predictive value
        npv = tn / (tn + fn) # negative preditive value
        acc = (tp + tn) / (tp + tn + fp + fn) # accuracy
        return acc, tpr, tnr, ppv, npv

    def signification(self, result, result_snake):
        return stats.kruskal(result,result_snake)

    def _get_error(self, result, top_line, bot_line):
        # Return Mean Square Error and Mean Absolute Error
        mse = mae = 0
        n = len(top_line) + len(bot_line)

        for x,y in top_line:
            if x >= result.lens_start_line and x <= result.lens_end_line:
                pred = result.get_lens_value(x)
                if pred > -1:
                    res = y - pred
                    mse += (res)**2
                    mae += abs(res)

        for x,y in bot_line:
            if x >= result.cornea_start_line and x <= result.cornea_end_line:
                pred = result.get_cornea_value(x)
                if pred > 1:
                    res = y - pred
                    mse += (res)**2
                    mae += abs(res)

        return mse/n, mae/n

    def _validate_result(self, result, eval_data, image):

        tp = fn = fp = tn = n = 0
        mse = mae = None
        #result.show(image, str(eval_data["has_lens"]) + " vs "  + str(result.has_lens))

        if eval_data["has_lens"] and result.has_lens:
            tp +=1
            mse, mae = self._get_error(result, eval_data["lens"], eval_data["cornea"])
        elif eval_data["has_lens"] and not result.has_lens:
            fn +=1
        elif not eval_data["has_lens"] and not result.has_lens:
            tn += 1
            mse, mae = self._get_error(result, eval_data["lens"], eval_data["cornea"])
        elif not eval_data["has_lens"]:
            fp += 1

        return mse, mae, tp, tn, fp, fn, eval_data["type"]

    def validate_snake(self, parameters):
        image_list, filter_list, names_list = utils._read_images(utils.TEST_PATH, utils.TESTJN_PATH)

        snake_mse_list = []
        snake_mae_list = []
        mse_list = []
        mae_list = []

        for i in range(0, len(image_list)):
            eval_data = utils.load_validation(names_list[i])
            if eval_data["has_lens"]:
                try:
                    result, result_snake, _ = PipeClass(parameters, verbose=False, snake_results=True).run(image_list[i], filter_list[i])
                except:
                    continue

                if result is not None and result_snake is not None:

                    mse, mae, _, _, _, _, _ = self._validate_result(result, eval_data, image_list[i])
                    mse_snake, mae_snake, _, _, _, _, _ = self._validate_result(result_snake, eval_data, image_list[i])

                    if mse and mae and mse_snake and mae_snake:
                        snake_mae_list.append(mae_snake)
                        snake_mse_list.append(mse_snake)
                        mae_list.append(mae)
                        mse_list.append(mse)

        h, p_value = self.signification(snake_mse_list,mse_list)
        print(h)
        print(p_value)
        h1, p_value1 = self.signification(snake_mae_list, mae_list)
        print(h1)
        print(p_value1)
        print("snake")
        print(np.median(np.array(snake_mae_list)))
        print(np.median(np.array(snake_mse_list)))
        print("pre")
        print(np.median(np.array(mae_list)))
        print(np.median(np.array(mse_list)))


    def validate(self,parameters):
        return self.validate1(parameters), self.validate1(parameters,utils.TEST_PATH, utils.TESTJN_PATH)

    def validate1(self, parameters, path_img = utils.CONFIG_PATH, path_jn = utils.CONFIGJN_PATH):

        image_list, filter_list, names_list = utils._read_images(path_img,path_jn)
        mse_list = []
        mae_list = []

        tiempo_total = {"preprocesado":{"tiempo":0, "mediciones":0},
                        "localizacion":{"tiempo":0, "mediciones":0},
                        "snake":{"tiempo":0, "mediciones":0},
                        "metricas":{"nearest":0,"vertical":0,"normal":0, "global":0, "mediciones":0},
                        "global": {"tiempo":0,"mediciones":0}}

        global_mae = global_mse = global_tp = global_tn = global_fp = global_fn =  0
        center_mae = center_mse = lateral_mae = lateral_mse = extreme_mae = extreme_mse = 0
        counter_center = counter_lateral = counter_extreme = counter = 0

        dict_data = {"CONFIG_ID": parameters.id}

        for i in range(0, len(image_list)):

            try:
                result, tiempo = PipeClass(parameters, verbose=False).run(image_list[i],filter_list[i])
            except:
                continue

            try:
                tiempo_metricas = MetricsClass(result).get_time()

                for key in tiempo_metricas:
                    tiempo_total["metricas"][key] += tiempo_metricas[key]
                    tiempo_total["metricas"]["mediciones"] += 1
            except:
                pass

            for key in tiempo:
                tiempo_total[key]["tiempo"] += tiempo[key]
                tiempo_total[key]["mediciones"] += 1

            eval_data = utils.load_validation(names_list[i])

            if result != None:

                mse, mae, tp, tn, fp, fn, type = self._validate_result(result,eval_data,image_list[i])

                if mae is not None:
                    counter += 1
                    mse_list.append(mse)
                    mae_list.append(mae)

                    global_mae += mae
                    global_mse += mse

                    if type == "c":
                        counter_center += 1
                        center_mae += mae
                        center_mse += mse
                    elif type == "l":
                        counter_lateral += 1
                        lateral_mae += mae
                        lateral_mse += mse
                    elif type == "e":
                        counter_extreme += 1
                        extreme_mae += mae
                        extreme_mse += mse

                global_tp += tp
                global_tn += tn
                global_fp += fp
                global_fn += fn

        acc, tpr, tnr, ppv, npv = self._get_metrics(global_tp,global_tn,global_fp,global_fn)

        dict_data["ACC"] = acc
        dict_data["AVG_MAE"] = global_mae / counter
        dict_data["AVG_MSE"] = global_mse / counter
        dict_data["CENTRAL_MAE"] = center_mae / counter_center
        dict_data["CENTRAL_MSE"] = center_mse / counter_center
        dict_data["LATERAL_MAE"] = lateral_mae / counter_lateral
        dict_data["LATERAL_MSE"] = lateral_mse / counter_lateral
        dict_data["EXTREME_MAE"] = extreme_mae / counter_extreme
        dict_data["EXTREME_MSE"] = extreme_mse / counter_extreme
        dict_data["TPR"] = tpr
        dict_data["TNR"] = tnr
        dict_data["PPV"] = ppv
        dict_data["NPV"] = npv
        dict_data["T_PREPROCESADO"] = tiempo_total["preprocesado"]["tiempo"]/tiempo_total["preprocesado"]["mediciones"]
        dict_data["T_LOCALIZACION"] = tiempo_total["localizacion"]["tiempo"]/tiempo_total["localizacion"]["mediciones"]
        dict_data["T_SNAKE"] = tiempo_total["snake"]["tiempo"]/tiempo_total["snake"]["mediciones"]
        dict_data["T_METRICAS"] = tiempo_total["metricas"]["global"]/tiempo_total["metricas"]["mediciones"]
        dict_data["T_NEAREST"] = tiempo_total["metricas"]["nearest"]/tiempo_total["metricas"]["mediciones"]
        dict_data["T_NORMAL"] = tiempo_total["metricas"]["normal"]/tiempo_total["metricas"]["mediciones"]
        dict_data["T_VERTICAL"] = tiempo_total["metricas"]["vertical"]/tiempo_total["metricas"]["mediciones"]
        dict_data["MEDIAN_MSE"] = np.median(np.array(mse_list))
        dict_data["MEDIAN_MAE"] = np.median(np.array(mae_list))
        dict_data["MAE"] = "\n" + str(mae_list)
        dict_data["MSE"] = "\n" + str(mse_list)

        return dict_data
