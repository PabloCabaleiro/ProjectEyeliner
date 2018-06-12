from Pipeline.process import ProccesClass
from Pipeline.preprocess import PreproccessClass
import time
from Pipeline.snake import SnakeClass
import matplotlib.pyplot as plt

class PipeClass():

    parameters = None
    verbose = False

    def __init__(self, parameters, verbose):
        self.parameters = parameters
        self.verbose = verbose

    def show_results(self, image, result, result_snake):
        plt.figure(1)
        plt.subplot(121)
        plt.imshow(image)
        plt.title("procesado")
        top = list(zip(*result.lens))
        plt.plot(top[0], top[1])
        bot = list(zip(*result.cornea))
        plt.plot(bot[0], bot[1])

        plt.subplot(122)
        plt.imshow(image)
        plt.title("snake")
        top = list(zip(*result_snake.lens))
        plt.plot(top[0], top[1])
        bot = list(zip(*result_snake.cornea))
        plt.plot(bot[0], bot[1])

        plt.show()


    def run(self,og_image,filter_image):


        preprocces = PreproccessClass(self.parameters)
        procces = ProccesClass(self.parameters)
        snake = SnakeClass(self.parameters)

        if self.verbose:
            start_time = time.time()
            print("\tPipeline:")

        rotated_img, enhanced_image, rotation_matrix = preprocces.pipeline(og_image, filter_image)

        if self.verbose:
            preprocess_time = time.time()
            print("\t\tTiempo preprocesado: " + str(preprocess_time - start_time) + "s")

        result = procces.pipeline(rotated_img, enhanced_image, rotation_matrix)

        if self.verbose:
            process_time = time.time()
            print("\t\tTiempo procesado: " + str(process_time - preprocess_time) + "s")

        if result.has_lens:
            result_snake = snake.run(og_image, result.lens, result.cornea)
            if self.verbose:
                snake_time = time.time()
                print("\t\tTiempo snake: " + str(snake_time - process_time) + "s")
                print("\t\tTiempo total: " + str(snake_time - start_time) + "s")
                self.show_results(og_image,result,result_snake)
            return result_snake

        elif self.verbose:
            print("\t\tTiempo total: " + str(process_time - start_time) + "s")

        return result
