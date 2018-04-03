from Pipeline.process import ProcessClass
from Pipeline.preprocess import PreproccessClass
from Utils.utils import _read_images


def main():
    image_list, names_list = _read_images()

    for i in range(0, len(image_list)):
        print(names_list[i])
        rotated_img, rotation_matrix = PreproccessClass(image_list[i]).pipeline()
        ProcessClass(rotated_img, rotation_matrix).pipeline()

if __name__ == '__main__':
    main()