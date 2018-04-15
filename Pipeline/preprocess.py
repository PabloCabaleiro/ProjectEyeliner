import cv2
import numpy as np
import matplotlib.pyplot as plt

RECTANGLE_POS = dict(big= [(20, 650), 180],  medium  = [(20, 600), 160], small = [(20, 470), 140])

BIG_SHAPE = (853, 1280)
MEDIUM_SHAPE = (786, 1180)
SMALL_SHAPE = (625, 938)

BIG_TYPE = "big"
MEDIUM_TYPE = "medium"
SMALL_TYPE = "small"

class PreproccessClass(object):

    img = None
    parameters = None

    def __init__(self, parameters):
        self.parameters = parameters

    def _rotate_bound(self, filter_image, angle):
        # grab the dimensions of the image and then determine the
        # center
        (h, w) = filter_image.shape[:2]
        (cX, cY) = (w // 2, h // 2)

        # grab the rotation matrix (applying the negative of the
        # angle to rotate clockwise), then grab the sine and cosine
        # (i.e., the rotation components of the matrix)
        M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])

        # compute the new bounding dimensions of the image
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))

        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY

        # perform the actual rotation and return the image
        return cv2.warpAffine(filter_image, M, (nW, nH)), M

    def _get_image_type(self, shape):
        if ((shape[0], shape[1]) == BIG_SHAPE):
            return BIG_TYPE
        elif ((shape[0], shape[1]) == MEDIUM_SHAPE):
            return MEDIUM_TYPE
        elif ((shape[0], shape[1]) == SMALL_SHAPE):
            return SMALL_TYPE
        else:
            return -1

    def _pre_get_masks(self, showMask=False):
        filter_img = cv2.GaussianBlur(self.img, (3, 3), 0)
        _, mask = cv2.threshold(filter_img, 5, 255, cv2.THRESH_BINARY)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((9, 9), np.uint8)
        open_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        kernel = np.ones((11, 11), np.uint8)
        dilated_img = cv2.morphologyEx(open_img, cv2.MORPH_ERODE, kernel)
        if showMask:
            cv2.imshow("Mask", dilated_img)
            cv2.waitKey()
        return dilated_img

    def _remove_UI(self):
        copy_img = self.img.copy()
        type = self._get_image_type(np.shape(self.img))
        if type != -1:
            initial_pos = RECTANGLE_POS[type][0]
            lenght = RECTANGLE_POS[type][1]
            kernel = np.ones((3, 3))
            open_img = cv2.morphologyEx(
                self.img[initial_pos[1]:initial_pos[1] + lenght, initial_pos[0]:initial_pos[0] + lenght], cv2.MORPH_OPEN,
                kernel)
            copy_img[initial_pos[1]:initial_pos[1] + lenght, initial_pos[0]:initial_pos[0] + lenght] = open_img
            return copy_img

    def _pre_median_bilateral(self, filter_image, bilateral_values, median_value):

        filter_img = cv2.medianBlur(filter_image, median_value)
        filter_img = cv2.bilateralFilter(filter_img, bilateral_values[0], bilateral_values[1], bilateral_values[2]);

        return filter_img

    def _hog_casero(self, blur_img, nbins=9, cell_size=(8, 8)):

        hist = np.zeros((nbins, 1))
        bin_size = int(360 / nbins)

        # Calculamos ángulo y magnitud
        gx = cv2.Sobel(blur_img, cv2.CV_32F, 1, 0, ksize=1)
        gy = cv2.Sobel(blur_img, cv2.CV_32F, 0, 1, ksize=1)
        mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)

        # Usar celdas -> más robusto a ruido y resultado más compacto

        for i in range(0, int(np.shape(mag)[0] / cell_size[0])):
            for j in range(0, int(np.shape(mag)[1] / cell_size[0])):
                # Calculamos ángulos y mangitudes medias para cada celda
                mean_mag = np.mean(mag[i * cell_size[0]:cell_size[0] * (i + 1), j * cell_size[1]:cell_size[1] * (
                j + 1)])  # Uso la media por lo que sigue sin ser robusto a ruido xd
                mean_angle = np.mean(
                    angle[i * cell_size[0]:cell_size[0] * (i + 1), j * cell_size[1]:cell_size[1] * (j + 1)])

                initial_pos = int(mean_angle / bin_size)
                weight = mean_angle / bin_size - initial_pos

                hist[initial_pos] += mean_mag * (1 - weight)
                if initial_pos < nbins - 1:
                    hist[initial_pos + 1] += mean_mag * weight
                else:
                    hist[0] += mean_mag * weight

        return hist, bin_size

    def _pre_rotate(self, filter_image, nbins=12, showRotation=False):

        blur_img = cv2.GaussianBlur(filter_image.copy(), ksize=(17, 17), sigmaX=100)

        hog, bin_size = self._hog_casero(blur_img, nbins=nbins)

        angle = bin_size * list(hog).index(max(hog))

        rotated_img, rotation_matrix = self._rotate_bound(filter_image, 90 - angle)

        if showRotation:
            plt.figure(1)
            plt.subplot(131)
            plt.imshow(self.img)
            plt.subplot(132)
            plt.axvline(x=90)
            plt.plot([v * bin_size for v in list(range(0, nbins))], hog)
            plt.subplot(133)
            plt.imshow(rotated_img)

            plt.show()

        return rotated_img, rotation_matrix

    def _pre_enhance_equalization(self,filter_img):

        img_yuv = cv2.cvtColor(filter_img, cv2.COLOR_BGR2YUV)

        # equalize the histogram of the Y channel
        img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])

        # convert the YUV image back to RGB format
        return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    def _pre_enhance_equalization_adaptative(self,filter_img):

        img_yuv = cv2.cvtColor(filter_img, cv2.COLOR_BGR2YUV)

        # equalize the histogram of the Y channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img_yuv[:, :, 0] = clahe.apply(img_yuv[:, :, 0])

        # convert the YUV image back to RGB format
        return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    def _pre_enhance_top_hat(self,filter_img):

        img_yuv = cv2.cvtColor(filter_img, cv2.COLOR_BGR2YUV)

        # equalize the histogram of the Y channel
        kernel = np.ones((15, 15), np.uint8)
        img_yuv[:, :, 0] = cv2.morphologyEx(img_yuv[:, :, 0],  cv2.MORPH_TOPHAT, kernel)

        # convert the YUV image back to RGB format
        return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)



    def pipeline(self, img):
        self.img = img

        filter_img = self._remove_UI()
        rotate_img, rotation_matrix = self._pre_rotate(filter_img, nbins=self.parameters.n_bins, showRotation=False)

        if self.parameters.enhance_function == "top_hat":
            enhanced_image = self._pre_enhance_top_hat(rotate_img)
        elif self.parameters.enhance_function == "equalization":
            enhanced_image = self._pre_enhance_equalization(rotate_img)
        else:
            enhanced_image = self._pre_enhance_equalization_adaptative(rotate_img)

        filter_img = self._pre_median_bilateral(enhanced_image, bilateral_values=(self.parameters.bilateral_diameter, self.parameters.sigma_color, self.parameters.sigma_space), median_value=self.parameters.median_value)
        return filter_img, enhanced_image, rotation_matrix