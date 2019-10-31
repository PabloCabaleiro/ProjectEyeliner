import cv2
import matplotlib.pyplot as plt
from matplotlib import transforms
import numpy as np
from Objects.ImageSegmentationClass import ImageSegmentationClass
from Objects.LayerClass import LayerClass
from Objects.ResultClass import ResultClass
from Utils import utils
from scipy import stats

class ProccesClass(object):

    filter_img = None
    width = None
    height = None
    mask = None
    parameters = None

    def __init__(self, parameters):
        self.parameters = parameters

    def _get_nearest_edge(self, edge_image, column, start_position):
        #####################################################################
        #Estimates the edge point on the next pixel based on previous points.
        #####################################################################

        #We establish a min and a max position where we can find the neares pixel corresponding to an edge.
        min_pos = start_position - self.parameters.localization_top_window
        max_pos = start_position + self.parameters.localization_bot_window

        #We find the edges on the column where we are trying to find the nearest point.
        diff = [int(edge_image[c,column]) - int(edge_image[c-1,column]) for c in range(min_pos + 1, max_pos)]
        ii = [min_pos + i for i in range(0,len(diff)) if diff[i] == 255]

        #If we don't find any edge on the column, we return -1
        if len(ii) == 0:
            return -1

        min = max_pos

        #We choose the point on the neares file from the previous point.
        for i in ii:
            if abs(i-start_position) < min:
                min = abs(i-start_position)
                result = i

        return result


    def _pre_get_masks(self):
        #####################################################################
        #Obtains the mask which exclude the non-interesting regions
        #####################################################################

        #Remove points with intensity < 5 after bluring the image.
        filter_img = cv2.GaussianBlur(self.filter_img, (3, 3), 0)
        _, mask = cv2.threshold(filter_img, 5, 255, cv2.THRESH_BINARY)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

        #We use a opening to remove the points in regions with many removed points aswell
        kernel = np.ones((9, 9), np.uint8)
        open_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        #We use a dilation to remove the edges between non-interesting regions and the images.
        kernel = np.ones((11, 11), np.uint8)
        dilated_img = cv2.morphologyEx(open_img, cv2.MORPH_ERODE, kernel)

        return dilated_img

    def _get_edges(self, kernel, canny_values, showEdges=False):
        #####################################################################
        #Obtains the edges of the image
        #####################################################################

        #Use canny to get the edges
        edge_img = cv2.Canny(self.filter_img, canny_values[0], canny_values[1])
        #Aply an opening to remove gaps inside the edges.
        edge_img = cv2.morphologyEx(edge_img, cv2.MORPH_CLOSE, kernel)

        if showEdges:
            cv2.imshow("Edges", edge_img)
            cv2.waitKey()

        return edge_img

    def _get_starting_pos(self, edge_img, row, previous_line, showStartingPos = False):
        #####################################################################
        #Obtains the first point that we use to aproximate pixel by pixel the edge.
        #####################################################################

        if previous_line != None:
            has_previous = True
        else:
            has_previous = False

        for i in range(0, self.width,10):

            #We check the points over the estimated row
            bottom_distance = -1
            for j in range(row,row+self.parameters.max_dist_to_roi):
                if edge_img[j,i] > 0:
                    if (not has_previous or j > previous_line.get_pos("bot", i) + self.parameters.edge_width) and self.check_point(edge_img,j,i):
                        bottom_distance = j
                        break
            #We check the points below the estimated row
            top_distance = -1
            for j in range(row, row-self.parameters.max_dist_to_roi,-1):
                if edge_img[j,i] > 0:
                    if (not has_previous or j > previous_line.get_pos("bot", i)) and self.check_point(edge_img,j,i):
                        top_distance = j
                        break
            #If we find a valid point we return the column of the nearest one
            if bottom_distance > -1 or top_distance > -1:
                start_column = i
                if showStartingPos:
                    plt.figure()
                    plt.plot(previous_line)
                    plt.imshow(self.filter_img)
                    plt.axvline(x=start_column)
                if (row - top_distance > bottom_distance - row) and bottom_distance > -1:
                    if showStartingPos:
                        plt.axhline(y=bottom_distance)
                        plt.show()
                    return bottom_distance, start_column
                else:
                    if showStartingPos:
                        plt.axhline(y=top_distance)
                        plt.show()
                    return top_distance, start_column
        return -1, -1

    def check_point(self, edge_image, x, y):
        #####################################################################
        #We check if the points seems to be an edge or may be noise.
        #####################################################################

        if sum(edge_image[x-5:x+5,y-10]) > 0 and sum(edge_image[x-5:x+5,y+10])>0:
            return True

        else:
            return False

    def _get_roi(self, edge_img, showRoi = False):
        #####################################################################
        #We obtain the Regions of interest in the images:
        #   * External edge of the lens
        #   * Internal edge of the lens
        #   * Cornea contour
        #####################################################################

        #We estimate the ROIs based on the study of the intensities across the rows.
        rows = [sum(edge_img[row, :]) for row in range(0, self.height)]
        #We derivate the intensities across the rows
        diff = [rows[c] - rows[c-1] for c in range(1, len(rows))]
        #We get the rows where it derivate is greater than the ROI threshold.
        roi = np.argwhere(np.array(diff) > self.parameters.roi_th)

        previous_result = -1
        result = []

        #We remove results too near to the previous one asuming that there are a min distance between edges.
        while len(roi) > 0:
            if previous_result == -1:
                previous_result = int(roi[0])
                result.append(previous_result)
            else:
                try:
                    previous_result = int(roi[roi > previous_result + self.parameters.min_dist_between_roi*self.height][0])
                    result.append(previous_result)
                except:
                    break

        if showRoi:
            plt.figure(1)
            plt.subplot(131)
            for row in result:
                plt.axhline(y=row)
            plt.imshow(edge_img)

            plt.subplot(132)
            plt.plot(rows)
            plt.subplot(133)
            plt.axhline(y=self.parameters.roi_th, c='g')
            plt.plot(diff)

            plt.show()

        return result

    def _rotate_back(self, top_line, bot_line, rotation_matrix):
        #####################################################################
        #We rotate back the detected edges obtained on the rotated images
        #####################################################################

        M = cv2.invertAffineTransform(rotation_matrix)

        top_line_ones = np.hstack([top_line, np.ones(shape=(len(top_line), 1))])
        bot_line_ones = np.hstack([bot_line, np.ones(shape=(len(bot_line), 1))])

        top_line_inv = M.dot(top_line_ones.T).T
        bot_line_inv = M.dot(bot_line_ones.T).T

        return top_line_inv, bot_line_inv

    def _get_top_line(self, edge_img, start_column, start_value, layers):
        #####################################################################
        #Obtains the top line of an edge píxel by pixel
        #####################################################################

        left_end = 0
        right_end = self.width
        top_line = [-1] * self.width
        gaps = []
        in_gap = False

        #We start the aproximation
        top_line[start_column] = start_value

        #We search first on the right
        for i in range(start_column + 1, self.width):

            #We obtain the next point based on the previous point
            pos = self._get_nearest_edge(edge_img, i, top_line[i - 1])

            #In case of a gap --> we don't find any edge on that column.
            if pos == -1:
                #We mantain the previous row on the next point only trying to not cross a previous line.
                if len(layers) > 0:
                    pos = max(top_line[i - 1], layers[-1].get_pos("bot", i))
                else:
                    pos = top_line[i - 1]

                #If we are on a gap and detect that we are in the non-interest image region, we stop.
                if self.mask[pos, i] == 0:
                    if sum(self.mask[pos, i:i + 10]) == 0:
                        if in_gap:
                            gaps.append((right_gap,i))
                        right_end = i
                        break

                #Else, if we weren't on a gap previously, we start one.
                if not in_gap:
                    in_gap = True
                    right_gap = i

            #If we find a point and were previously on a gap, we close it.
            elif in_gap:
                gaps.append((right_gap, i))
                in_gap = False

            #We save the detected points.
            top_line[i] = pos

        in_gap = False

        #Now we search the left points from the start column.
        for i in range(start_column - 1, -1, -1):

            # We obtain the next point based on the previous point
            pos = self._get_nearest_edge(edge_img, i, top_line[i + 1])

            # In case of a gap --> we don't find any edge on that column.
            if pos == -1:  # GAP
                # We mantain the previous row on the next point only trying to not cross a previous line.
                if len(layers) > 0:
                    try:
                        pos = max(top_line[i + 1], layers[-1].get_pos("bot", i))
                    except:
                        pos = top_line[i + 1]
                else:
                    pos = top_line[i + 1]

                # If we are on a gap and detect that we are in the non-interest image region, we stop.
                if self.mask[pos, i] == 0:
                    if sum(self.mask[pos, i - 10:i]) == 0:
                        if in_gap:
                            gaps.append((i,left_gap))
                        left_end = i
                        break

                # Else, if we weren't on a gap previously, we start one.
                if not in_gap:
                    in_gap = True
                    left_gap = i

            # If we find a point and were previously on a gap, we close it.
            elif in_gap:
                gaps.append((i, left_gap))
                in_gap = False

            # We save the detected points.
            top_line[i] = pos

        # We check if the line seems to be ok or it has many gaps.
        if self._check_line(top_line, gaps, left_end, right_end):
            # If it seems ok we save it
            layer = LayerClass()
            layer.set_top_line(top_line[left_end+1:right_end-1], left_end+1, right_end-1)
            layer.set_gaps(gaps)
            layer.interpolate_gaps()
            return layer
        else:
            # If the line seems to be noise, we return None.
            return None

    def _get_bot_line(self, edge_img, layer):
        #####################################################################
        # We obtain the bot line of an edge based on the top line and the edge information.
        #####################################################################

        result = []
        # We find the external pixel of an detected edge. We use a min distance representing the width of the edge
        # and a max distance where we look for a candidate point.
        for i in range(layer.get_start(), layer.get_end()):
            y = layer.get_pos("top",i)
            aux = [int(edge_img[j, i]) - int(edge_img[j - 1, i]) for j in
                   range(y + self.parameters.edge_width, y + self.parameters.edge_width + self.parameters.sample_window)]
            result.append(int(np.argmax(np.array(aux) < 0) + y + self.parameters.edge_width))

        return result

    def _check_line(self, line, gaps, left_end, right_end):
        #####################################################################
        # We estimate if the obtained line seems ok or not based on its gaps.
        #####################################################################

        # If there are too many gaps --> It's not a real line.
        total_gap = sum([y-x for x,y in gaps])
        total_line = right_end - left_end
        if total_gap/total_line > 0.5:
            return False
        else:
            return True

    def _check_cornea(self, layer, enhanced_img):
        #####################################################################
        # We obtain the difference between the intesities over the layer and below and layer.
        #####################################################################

        top_line = layer.top_line

        diff = np.mean([int(np.sum(enhanced_img[(int(top_line[k][1]) + self.parameters.edge_width*3):(
        int(top_line[k][1]) + self.parameters.edge_width*3 + self.parameters.sample_window), top_line[k][0]])) - int(
            np.sum(enhanced_img[(int(top_line[k][1]) - self.parameters.sample_window):int(top_line[k][1]), top_line[k][0]])) for k in
                        range(0, len(top_line))])

        return diff

    def _localization(self, edge_img, enhanced_img, showImgs=False):
        #####################################################################
        # Main function of the preliminar localization phase.
        #####################################################################

        self.height, self.width = np.shape(edge_img)

        # We estimate the rows where we can find regions of interest.
        rows = self._get_roi(edge_img,showRoi=False)
        N_ROWS = len(rows)

        n_capas = 0
        n_rows = 0

        diffs = []
        layers = []

        # We aproximate the previously obtained rows to the edges of the image.
        while n_capas < self.parameters.n_roi and n_rows < N_ROWS:
            # We find a valid position to start.
            if len(layers) == 0:
                start_value, start_column = self._get_starting_pos(edge_img,rows[n_rows],None,showStartingPos=False)
            else:
                start_value, start_column = self._get_starting_pos(edge_img,rows[n_rows],layers[-1],showStartingPos=False)

            if start_column != -1:

                # We get the top line
                layer = self._get_top_line(edge_img,start_column,start_value,layers)

                if layer != None:

                    # We get the information to know if it represents the cornea
                    diffs.append(self._check_cornea(layer, enhanced_img))

                    if n_capas == self.parameters.n_roi - 1:
                        layers.append(layer)
                        break

                    #We get the bot line
                    layer.set_bot_line(self._get_bot_line(edge_img,layer))

                    # We save the layer.
                    layers.append(layer)

                else:
                    n_rows +=1
                    continue
            else:
                n_rows += 1
                continue

            n_capas += 1
            n_rows += 1

        #We save the whole segmentation with all the layers detected.
        seg = ImageSegmentationClass(layers,diffs)

        if showImgs:
            seg.show(edge_img,enhanced_img)

        return seg

    def pipeline(self, filter_img, enhanced_img, rotation_matrix):
        #####################################################################
        # Pipeline of the preliminar localization phase.
        #####################################################################

        self.filter_img = filter_img
        self.height, self.width, _ = np.shape(filter_img)

        # We obtain the mask of the rotated images.
        self.mask = self._pre_get_masks()

        # We get the edge image from the rotated images.
        edge_img = self._get_edges(np.ones((self.parameters.canny_kernel, self.parameters.canny_kernel), np.uint8), (self.parameters.canny_inf, self.parameters.canny_sup) , showEdges=False)

        # We remove the edges corresponding to the border of the image.
        edge_img = cv2.bitwise_or(edge_img, edge_img, mask=self.mask)

        # We try to aproximate the regions of interest.
        segmentation = self._localization(edge_img, enhanced_img, showImgs=False)

        top_line, bot_line, has_lens = segmentation.get_result()

        # We rotate back the detected points.
        top_line, bot_line = self._rotate_back(top_line,bot_line, rotation_matrix)

        # We round the ouput of the rotate_back step.
        top_line, bot_line = utils.fpoints2ipoints(top_line, bot_line)

        return ResultClass(top_line,bot_line,has_lens)
