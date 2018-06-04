from Pipeline.Pipe import PipeClass
from Utils.utils import _read_images
from Utils.parameter_manager import ParameterManagerClass
from Validation.validate_configuration import ValidateConfiguration
from Metrics.metrics import MetricsClass
import csv
import matplotlib.pyplot as plt
from Utils import utils

def main(verbose):

    parameters = ParameterManagerClass() #default

    image_list, names_list = _read_images()

    for i in range(0, len(image_list)):

        if verbose:
            print(names_list[i])

        result_snake = PipeClass(parameters, verbose=verbose).run(image_list[i])
        #if result_snake.has_lens:
        #    metrics = MetricsClass(result_snake, verbose=verbose)
        #    metrics.show_distances(image_list[i])

    # data = ValidateConfiguration().validate(parameters)
    # first = True
    #
    # with open(utils.VAL_PATH + "result_data.csv", 'a') as csvfile:
    #     writer = csv.DictWriter(csvfile, data.keys())
    #     if first:
    #         writer.writeheader()
    #     writer.writerow(data)






if __name__ == '__main__':
    main(verbose=True)