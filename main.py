from Pipeline.process import ProccesClass
from Pipeline.preprocess import PreproccessClass
from Utils.utils import _read_images
import matplotlib.pyplot as plt
from Utils.parameter_manager import ParameterManagerClass


def main():
    parameters = ParameterManagerClass() #default

    image_list, names_list = _read_images()
    preprocces = PreproccessClass(parameters)
    procces = ProccesClass(parameters)

    for i in range(0, len(image_list)):
        print(names_list[i])
        rotated_img, rotation_matrix = preprocces.pipeline(image_list[i])
        result = procces.pipeline(rotated_img, rotation_matrix)
        result.show(image_list[i])


if __name__ == '__main__':
    main()