import cv2
import numpy as np
import matplotlib.pyplot as plt
import Utils.utils

RECTANGLE_POS = dict(big= [(20, 650), 180],  medium  = [(20, 600), 160], small = [(20, 470), 140])

BIG_SHAPE = (853, 1280)
MEDIUM_SHAPE = (786, 1180)
SMALL_SHAPE = (625, 938)

BIG_TYPE = "big"
MEDIUM_TYPE = "medium"
SMALL_TYPE = "small"

class PreproccessClass(object):

    parameters = None

    def __init__(self, parameters):
        self.parameters = parameters

    def _rotate_bound(self, filter_image, og_img, angle):
        ############################################################################################
        # Rotates the filter images
        ############################################################################################

        #https://www.pyimagesearch.com/2017/01/02/rotate-images-correctly-with-opencv-and-python/
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
        return cv2.warpAffine(filter_image, M, (nW, nH)),cv2.warpAffine(og_img, M, (nW, nH)), M

    def _get_image_type(self, shape):
        ############################################################################################
        # Detects the size of the image to remove the UI
        ############################################################################################
        if ((shape[0], shape[1]) == BIG_SHAPE):
            return BIG_TYPE
        elif ((shape[0], shape[1]) == MEDIUM_SHAPE):
            return MEDIUM_TYPE
        elif ((shape[0], shape[1]) == SMALL_SHAPE):
            return SMALL_TYPE
        else:
            return -1

    def _pre_get_masks(self, img, showMask=False):
        ############################################################################################
        # Gets the mask of the non interest region.
        ############################################################################################
        filter_img = cv2.GaussianBlur(img, (3, 3), 0)
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

    def _remove_UI(self, img):
        ############################################################################################
        # Removes the ui of the image
        ############################################################################################
        type = self._get_image_type(np.shape(img))
        if type != -1:
            initial_pos = RECTANGLE_POS[type][0]
            lenght = RECTANGLE_POS[type][1]
            kernel = np.ones((3, 3))
            open_img = cv2.morphologyEx(
                img[initial_pos[1]:initial_pos[1] + lenght, initial_pos[0]:initial_pos[0] + lenght], cv2.MORPH_OPEN,
                kernel)
            img[initial_pos[1]:initial_pos[1] + lenght, initial_pos[0]:initial_pos[0] + lenght] = open_img
        return img

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

    def _pre_rotate(self, og_img, filter_image, nbins=12, showRotation=False):

        blur_img = cv2.GaussianBlur(filter_image.copy(), ksize=(17, 17), sigmaX=100)

        hog, bin_size = self._hog_casero(blur_img, nbins=nbins)

        angle = bin_size * list(hog).index(max(hog))

        rotated_img, rotated_og, rotation_matrix = self._rotate_bound(filter_image, og_img, 90 - angle)

        if showRotation:
            plt.figure(1)
            plt.subplot(131)
            plt.imshow(og_img)
            plt.subplot(132)
            plt.axvline(x=90, color="r", linestyle='dashed')
            plt.plot([v * bin_size for v in list(range(0, nbins))], hog)
            plt.subplot(133)
            plt.imshow(rotated_img)

            plt.show()

        return rotated_img, rotated_og, rotation_matrix

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
        kernel = np.ones((self.parameters.top_hat_kernel, self.parameters.top_hat_kernel), np.uint8)
        img_yuv[:, :, 0] = cv2.morphologyEx(img_yuv[:, :, 0],  cv2.MORPH_TOPHAT, kernel)

        # convert the YUV image back to RGB format
        return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    def _weird_enhancement(self, filter_img):
        width = np.shape(filter_img)[0]
        height = np.shape(filter_img)[1]
        aux_img = filter_img.copy()

        for i in range(0, width):
            for j in range(0,height):
                if sum(filter_img[i,j]) > 0:
                    region = filter_img[max(0,i-5):min(width-1,i+5),max(0,j-5):min(height-1,j+5),1]
                    aux_img[i,j,1] = 2*filter_img[i,j,1] - np.mean(region) + (100*np.min(region)/(np.max(region)+1))

        return aux_img


    def pipeline(self, img, filter_img):

        filter_img = self._remove_UI(filter_img)
        enhanced_image = self._pre_enhance_top_hat(filter_img)
        #self.show(filter_img,enhanced_image)
        rotate_img, enhanced_image, rotation_matrix = self._pre_rotate(enhanced_image, filter_img, nbins=self.parameters.n_bins, showRotation=False)



        #filter_img = self._pre_median_bilateral(enhanced_image, bilateral_values=(self.parameters.bilateral_diameter, self.parameters.sigma_color, self.parameters.sigma_space),
        #median_value=self.parameters.median_value)
        #self.show(filter_img, name="filter")
        return rotate_img, enhanced_image, rotation_matrix

    def show(self, image, image2=None, name = None):
        if name is None:
            plt.figure("Rotated image segmentation")
        else:
            plt.figure(name)

        plt.subplot(121)
        plt.imshow(image)
        plt.subplot(122)
        plt.imshow(image2)

        plt.show()