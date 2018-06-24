import numpy as np
from Objects.ResultClass import ResultClass
from skimage.segmentation import active_contour
from Utils.utils import fpoints2ipoints
class SnakeClass(object):

    parameters = None

    def __init__(self, parameters):
        self.parameters = parameters

    def snake(self, image, lens, cornea):
        points_lens = np.array([[int(x),int(y)] for x,y in lens[1:-1]])
        points_cornea = np.array([[int(x),int(y)] for x,y in cornea[1:-1]])
        snake_lens = active_contour(image, points_lens, alpha= self.parameters.alpha, beta= self.parameters.beta, w_line= self.parameters.w_line,
                                    w_edge= self.parameters.w_edge, gamma= self.parameters.gamma, bc="fixed")
        snake_cornea = active_contour(image, points_cornea, alpha= self.parameters.alpha, beta= self.parameters.beta, w_line= self.parameters.w_line,
                                      w_edge= self.parameters.w_edge, gamma=self.parameters.gamma, bc="fixed")

        return snake_lens, snake_cornea

    def run(self, image, top_line, bot_line):

        lens_snake, cornea_snake = self.snake(image, top_line, bot_line)
        lens_snake, cornea_snake = fpoints2ipoints(lens_snake, cornea_snake)

        return ResultClass(lens_snake, cornea_snake, True)
