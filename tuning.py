from Utils.parameter_manager import ParameterManagerClass
from Validation.validate_configuration import ValidateConfiguration
from Utils import utils
import csv
from scipy.optimize import differential_evolution
import sys

MEDIAN_LIST = [3,5,7,9]
BILATERAL_DIAMETER = [5,7,9,11,13,15,17,19,21]
TOP_HAT_KERNEL = [15,17,19,21,23,25,27,29,21,33,35]


def func(parameters,*data):
    roi_th = int(round(parameters[0]))
    median = MEDIAN_LIST[int(round(parameters[1]))]
    sigma_color = int(round(parameters[2]))
    sigma_space = int(round(parameters[3]))
    bilateral_diameter = BILATERAL_DIAMETER[int(round(parameters[4]))]
    top_hat_kernel_size = TOP_HAT_KERNEL[int(round(parameters[5]))]
    canny_sup = int(round(parameters[6]))
    canny_inf = int(round(parameters[7]))
    canny_kernel = MEDIAN_LIST[int(round(parameters[8]))]

    parameters = ParameterManagerClass(roi_th=roi_th,median_value=median,
                                       sigma_color=sigma_color,sigma_space=sigma_space,bilateral_diameter=bilateral_diameter,top_hat_kernel=top_hat_kernel_size,
                                       canny_sup=canny_sup,canny_inf=canny_inf,canny_kernel=canny_kernel)

    try:

        with open(utils.VAL_PATH + "configuration_data.csv", 'a') as csvfile:
            params_dict = parameters.get_config()
            writer = csv.DictWriter(csvfile, params_dict.keys())
            writer.writeheader()
            writer.writerow(params_dict)

        data = ValidateConfiguration().validate(parameters)

        with open(utils.VAL_PATH + "result_data.csv", 'a') as csvfile:
            writer = csv.DictWriter(csvfile, data.keys())
            writer.writeheader()
            writer.writerow(data)

        result =  data["AVG_MSE"] / data["ACC"]
        print("AVG_MSE: " + str(data["AVG_MSE"]) + " ACC: " + str(data["ACC"]))
        return result

    except:
        print("Unexpected error:", sys.exc_info())
        return 50000




if __name__ == '__main__':

    bounds = []
    bounds.append((2000,5000))
    bounds.append((0,3))
    bounds.append((100,250))
    bounds.append((100,250))
    bounds.append((0,8))
    bounds.append((0,10))
    bounds.append((40,100))
    bounds.append((20,80))
    bounds.append((0,3))

    result = differential_evolution(func, bounds, args=[])
    print(result.x)
    print(result)