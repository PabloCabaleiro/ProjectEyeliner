import matplotlib.pyplot as plt

class ImageSegmentationClass(object):

    layers = None
    _complete = False

    def __init__(self):
        self.layers = []

    def add_layer(self, layer):
        self.layers.append(layer)
        if layer.is_retina:
            self._complete = True

    def is_completed(self):
        return self._complete

    def get_last_bot_line(self, pos = -1):

        if len(self.layers) == 0:
            return -1
        elif pos == -1:
            return self.layers[-1]
        else:
            return self.layers[-1].get_pos("bot", pos)

    def show(self, image):
        plt.figure("Rotated image segmentation")
        for layer in self.layers:
            top = list(zip(*layer.top_line))
            plt.plot(top[0],top[1])
            bot = list(zip(*layer.bot_line))
            plt.plot(bot[0],bot[1])
        plt.imshow(image)
        plt.show()
