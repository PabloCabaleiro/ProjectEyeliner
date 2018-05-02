from Pipeline.Pipe import PipeClass
from Utils.utils import _read_images
from Utils.parameter_manager import ParameterManagerClass
from Metrics.metrics import MetricsClass
import time

def main(verbose):

    parameters = ParameterManagerClass() #default

    image_list, names_list = _read_images()

    for i in range(0, len(image_list)):

        if verbose:
            print(names_list[i])

        result = PipeClass(parameters, verbose=verbose).run(image_list[i])

        if result.has_lens:
            metrics = MetricsClass(result, verbose=verbose)
            metrics.show_distances(image_list[i])

if __name__ == '__main__':
    main(verbose=True)