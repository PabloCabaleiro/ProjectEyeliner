from Pipeline.Pipe import PipeClass
from Utils.utils import _read_images
from Utils.parameter_manager import ParameterManagerClass
from Metrics.metrics import MetricsClass
import time
import matplotlib.pyplot as plt

def main(verbose):

    parameters = ParameterManagerClass() #default

    image_list, names_list = _read_images()

    for i in range(0, len(image_list)):

        if verbose:
            print(names_list[i])

        result, result_snake = PipeClass(parameters, verbose=verbose).run(image_list[i])

        plt.figure(1)
        plt.subplot(121)
        plt.imshow(image_list[i])

        top = list(zip(*result.lens))
        plt.plot(top[0], top[1])
        bot = list(zip(*result.cornea))
        plt.plot(bot[0], bot[1])

        plt.subplot(122)
        plt.imshow(image_list[i])

        top = list(zip(*result_snake.lens))
        plt.plot(top[0], top[1])
        bot = list(zip(*result_snake.cornea))
        plt.plot(bot[0], bot[1])

        plt.show()

if __name__ == '__main__':
    main(verbose=True)