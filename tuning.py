from Utils.parameter_manager import ParameterManagerClass
from Validation.validate_configuration import ValidateConfiguration
from Utils import utils
import csv
from scipy.optimize import differential_evolution
import sys

MEDIAN_LIST = [3,5,7,9]
BILATERAL_DIAMETER = [5,7,9,11,13,15,17,19,21]
TOP_HAT_KERNEL = [9,11,13,15,17,19,21,23,25,27,29,21,33,35]


def func(parameters,*data):
    cornea_th = round(parameters[0])
    roi_th = round(parameters[1])
    beta = parameters[2]
    alpha = parameters[3]
    w_edge = parameters[4]
    gamma = parameters[5]
    median = MEDIAN_LIST[int(round(parameters[6]))]
    sigma_color = round(parameters[7])
    sigma_space = round(parameters[8])
    bilateral_diameter = BILATERAL_DIAMETER[int(round(parameters[9]))]
    top_hat_kernel_size = TOP_HAT_KERNEL[int(round(parameters[10]))]
    canny_sup = round(parameters[11])
    canny_inf = round(parameters[12])
    canny_kernel = MEDIAN_LIST[int(round(parameters[13]))]

    parameters = ParameterManagerClass(cornea_th=cornea_th,roi_th=roi_th,beta=beta,alpha=alpha,w_edge=w_edge,gamma=gamma,median_value=median,
                                       sigma_color=sigma_color,sigma_space=sigma_space,bilateral_diameter=bilateral_diameter,top_hat_kernel=top_hat_kernel_size,
                                       canny_sup=canny_sup,canny_inf=canny_inf,canny_kernel=canny_kernel)

    try:
        data = ValidateConfiguration().validate(parameters)
    except:
        print("Unexpected error:", sys.exc_info()[0])


    with open(utils.VAL_PATH + "result_data.csv", 'a') as csvfile:
        writer = csv.DictWriter(csvfile, data.keys())
        writer.writerow(data)

    return data["AVG_MSE"]/data["ACC"]




if __name__ == '__main__':

    bounds = []
    bounds.append((20,40))
    bounds.append((2000,5000))
    bounds.append((5,70))
    bounds.append((5,70))
    bounds.append((0,30))
    bounds.append((0,5))
    bounds.append((0,3))
    bounds.append((100,250))
    bounds.append((100,250))
    bounds.append((0,8))
    bounds.append((0,13))
    bounds.append((40,100))
    bounds.append((20,80))
    bounds.append((0,3))

    result = differential_evolution(func, bounds, args=[])
    print(result.x)
    print(result)