from Pipeline.process import ProcessClass
from Pipeline.preprocess import PreproccessClass
from Utils.utils import _read_images
import matplotlib.pyplot as plt


def main():
    image_list, names_list = _read_images()

    for i in range(0, len(image_list)):
        print(names_list[i])
        rotated_img, rotation_matrix = PreproccessClass(image_list[i]).pipeline()
        result = ProcessClass(rotated_img, rotation_matrix).pipeline()
        plt.figure()
        plt.imshow(image_list[i])
        top = list(zip(*result.lens))
        plt.plot(top[0], top[1])
        bot = list(zip(*result.cornea))
        plt.plot(bot[0], bot[1])
        plt.show()

if __name__ == '__main__':
    main()