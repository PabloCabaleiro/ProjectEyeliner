import matplotlib.pyplot as plt

class ImageSegmentationClass(object):

    layers = None
    _complete = False

    def __init__(self, layers, diff=None):

        if diff is None:
            self.layers = layers
            self._complete= True
            self.layers[-1].is_retina = True

        elif len(diff) > 1:

            self.layers = []

            index = diff.index(max(diff[1:]))

            for i in range(0, index +1):
                if i == index:
                    layer = layers[i]
                    layer.is_retina = True
                    self.add_layer(layer)
                    self._complete = True
                else:
                    self.add_layer(layers[i])


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

    def get_result(self):
        if self.layers is not None and len(self.layers) == 3:
            return self.layers[-2].bot_line, self.layers[-1].top_line, True
        elif self.layers is not None and len(self.layers) == 2:
            return self.layers[-2].bot_line, self.layers[-1].top_line, False
        else:
            return None, None, False

    def show(self, image, image2=None, name = None):
        if name:
            plt.figure(name)
        else:
            plt.figure("Rotated image segmentation")

        if image2 is not None:
            plt.subplot(121)

        for layer in self.layers:
            top = list(zip(*layer.top_line))
            plt.plot(top[0],top[1])
            if not layer.is_retina:
                bot = list(zip(*layer.bot_line))
                plt.plot(bot[0],bot[1])
        plt.imshow(image)

        if image2 is not None:
            plt.subplot(122)
            for layer in self.layers:
                top = list(zip(*layer.top_line))
                plt.plot(top[0], top[1])
                if not layer.is_retina:
                    bot = list(zip(*layer.bot_line))
                    plt.plot(bot[0], bot[1])
            plt.imshow(image2)

        plt.show()
