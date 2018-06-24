from Utils.parameter_manager import ParameterManagerClass
from Validation.validate_configuration import ValidateConfiguration
from Utils import utils
import csv
from scipy.optimize import differential_evolution
import sys

MEDIAN_LIST = [3,5,7,9]
BILATERAL_DIAMETER = [5,7,9,11,13,15,17,19,21]
TOP_HAT_KERNEL = [15,17,19,21,23,25,27,29,21,33,35]
ROI_TH = [2700,2800,2900,3000,3100,3200]
SIGMA = [100,125,150,175,200,225,250,275,300,325]
CANNY_SUP = [70,80,90,100,110,120,130,140,150,160]
CANNY_INF = [40,50,60,70,80,90,100,110,120,130]
LOCALIZATION_WINDOW = [5,7,10,12,15,20]

def func(parameters,*data):
    roi_th = ROI_TH[int(round(parameters[0]))]
    median = MEDIAN_LIST[int(round(parameters[1]))]
    top_hat_kernel_size = TOP_HAT_KERNEL[int(round(parameters[2]))]
    canny_sup = CANNY_SUP[int(round(parameters[3]))]
    canny_inf = CANNY_INF[int(round(parameters[4]))]
    canny_kernel = MEDIAN_LIST[int(round(parameters[5]))]
    top_window = bot_window = LOCALIZATION_WINDOW[int(round(parameters[6]))]

    parameters = ParameterManagerClass(roi_th=roi_th,median_value=median,
                                       top_hat_kernel=top_hat_kernel_size, max_dist_top= top_window, max_dist_bot = bot_window,
                                       canny_sup=canny_sup,canny_inf=canny_inf,canny_kernel=canny_kernel)

    try:
        values = {}
        with open(utils.VAL_PATH + "results.csv", 'r') as csvfile:
            for line in csvfile:
                if line != "\n":
                    list = line.replace("\n","").split(",")
                    values[list[0]] = list[1]

        for val in values:
            if val == parameters.get_id():
                return values[val]

        with open(utils.VAL_PATH + "configuration_data.csv", 'a') as csvfile:
            params_dict = parameters.get_config()
            writer = csv.DictWriter(csvfile, params_dict.keys())
            writer.writeheader()
            writer.writerow(params_dict)

        data1 = ValidateConfiguration().validate(parameters)

        with open(utils.VAL_PATH + "result_data.csv", 'a') as csvfile:
            writer = csv.DictWriter(csvfile, data1.keys())
            writer.writeheader()
            writer.writerow(data1)
            #writer.writerow(data2)

        result =  1- data1["ACC"]
        print(parameters.id + "\t" "AVG_MSE: " + str(data1["AVG_MSE"]) + " ACC: " + str(data1["ACC"]) + "\n")
        with open(utils.VAL_PATH + "log.txt", 'a') as f:
            f.write(parameters.id + "\t" "AVG_MSE: " + str(data1["AVG_MSE"]) + " ACC: " + str(data1["ACC"]) + "\n")
            #f.write(parameters.id + "\t" "AVG_MSE: " + str(data2["AVG_MSE"]) + " ACC: " + str(data2["ACC"]) + "\n")
            f.write("\n")

        with open(utils.VAL_PATH + "results.csv", 'a') as csvfile:
            writer = csv.DictWriter(csvfile, ["id","value"])
            writer.writerow({"id": parameters.get_id(), "value": result})

        return result
    except:
        pass





if __name__ == '__main__':

    bounds = []
    bounds.append((0,5))        #roi_th
    bounds.append((0,3))        #median
    bounds.append((0,10))       #top_hat_kernel
    bounds.append((0,9))        #canny_sup
    bounds.append((0,9))        #canny_inf
    bounds.append((0,3))        #canny_kernel
    bounds.append((0,5))

    with open(utils.VAL_PATH + "results.csv", 'a') as csvfile:
        writer = csv.DictWriter(csvfile,["id","value"])

    result = differential_evolution(func, bounds, args=[])