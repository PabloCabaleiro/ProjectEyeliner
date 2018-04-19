from Pipeline.Pipe import PipeClass
from Utils.utils import _read_images
from Utils.parameter_manager import ParameterManagerClass


def main():
    parameters = ParameterManagerClass() #default

    image_list, names_list = _read_images()

    for i in range(0, len(image_list)):
        print(names_list[i])
        result = PipeClass(parameters).run(image_list[i])
        result.show(image_list[i])


if __name__ == '__main__':
    main()