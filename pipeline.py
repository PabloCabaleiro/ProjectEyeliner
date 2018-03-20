from preprocess import PreproccessClass
from proccess import ProccessClass
from utils import _read_images

class PipelineClass(object):

    def run(self):
        image_list, names_list = _read_images()

        for img in image_list:
            rotated_img, rotation_matrix = PreproccessClass(img).pipeline()
            ProccessClass(rotated_img).pipeline()

