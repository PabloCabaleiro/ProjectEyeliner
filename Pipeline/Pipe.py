from Pipeline.process import ProccesClass
from Pipeline.preprocess import PreproccessClass
import time

class PipeClass():

    parameters = None
    verbose = False

    def __init__(self, parameters, verbose):
        self.parameters = parameters
        self.verbose = verbose

    def run(self,image):


        preprocces = PreproccessClass(self.parameters)
        procces = ProccesClass(self.parameters)

        if self.verbose:
            start_time = time.time()
            print("\tPipeline:")

        rotated_img, enhanced_image, rotation_matrix = preprocces.pipeline(image)

        if self.verbose:
            preprocess_time = time.time()
            print("\t\tTiempo preprocesado: " + str(preprocess_time - start_time) + "s")

        result = procces.pipeline(rotated_img, enhanced_image, rotation_matrix)

        if self.verbose:
            process_time = time.time()
            print("\t\tTiempo procesado: " + str(process_time - preprocess_time) + "s")
            print("\t\tTiempo total: " + str(process_time - start_time) + "s")


        return result
