from preprocess import PreproccessClass
from proccess import ProccessClass
from utils import _read_images

class PipelineClass(object):

    def run(self):
        image_list, names_list = _read_images()

        for i in range(0,len(image_list)):
            print(names_list[i])
            rotated_img, rotation_matrix = PreproccessClass(image_list[i]).pipeline()
            ProccessClass(rotated_img).pipeline()

