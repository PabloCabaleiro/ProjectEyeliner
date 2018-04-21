from Pipeline.process import ProccesClass
from Pipeline.preprocess import PreproccessClass

class PipeClass():

    parameters = None

    def __init__(self, parameters):
        self.parameters = parameters

    def run(self,image):

        preprocces = PreproccessClass(self.parameters)
        procces = ProccesClass(self.parameters)

        rotated_img, enhanced_image, rotation_matrix = preprocces.pipeline(image)
        return procces.pipeline(rotated_img, enhanced_image, rotation_matrix)
