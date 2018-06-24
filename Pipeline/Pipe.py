from Pipeline.process import ProccesClass
from Pipeline.preprocess import PreproccessClass
import time
from Pipeline.snake import SnakeClass
import matplotlib.pyplot as plt

class PipeClass():

    parameters = None
    verbose = False
    snake_results = False

    def __init__(self, parameters, verbose, snake_results = False):
        self.parameters = parameters
        self.verbose = verbose
        self.snake_results = snake_results

    def show_results(self, image, result, result_snake = None):
        plt.figure(1)
        plt.subplot(121)
        plt.imshow(image)
        plt.title("procesado")
        top = list(zip(*result.lens))
        plt.plot(top[0], top[1])
        bot = list(zip(*result.cornea))
        plt.plot(bot[0], bot[1])

        if result_snake is not None:
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
        tiempo = {}

        start_time = time.time()
        if self.verbose:
            print("\tPipeline:")

        rotated_img, enhanced_image, rotation_matrix = preprocces.pipeline(og_image, filter_image)

        preprocess_time = time.time()
        if self.verbose:
            print("\t\tTiempo preprocesado: " + str(preprocess_time - start_time) + "s")
        tiempo["preprocesado"] = preprocess_time - start_time

        result = procces.pipeline(rotated_img, enhanced_image, rotation_matrix)

        process_time = time.time()
        if self.verbose:
            print("\t\tTiempo procesado: " + str(process_time - preprocess_time) + "s")
        tiempo["localizacion"] = process_time - preprocess_time

        if result.has_lens:
            try:
                result_snake = snake.run(og_image, result.lens, result.cornea)
                snake_time = time.time()
                if self.verbose:
                    print("\t\tTiempo snake: " + str(snake_time - process_time) + "s")
                    print("\t\tTiempo total: " + str(snake_time - start_time) + "s")
                    self.show_results(og_image,result,result_snake)
                tiempo["snake"] = snake_time - process_time
                tiempo["global"] = snake_time - start_time

                if self.snake_results:
                    return result, result_snake, tiempo

                return result_snake, tiempo

            except Exception as e:
                print(e)
                result = None

        elif self.verbose:
            tiempo["global"] = process_time - start_time
            print("\t\tTiempo total: " + str(process_time - start_time) + "s")

        if self.snake_results:
            return result, None, tiempo

        return result, tiempo
