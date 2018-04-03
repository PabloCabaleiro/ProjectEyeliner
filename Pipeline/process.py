import cv2
import matplotlib.pyplot as plt
import numpy as np
from Objects.ImageSegmentationClass import ImageSegmentationClass
from Objects.LayerClass import LayerClass

RETINA_TH = 27          # Diferencia de intensidad umbral para ser retina entre los vectores de SAMPLE_SIZE
MIN_DIST_CAPAS = 20     # Distancia mínima entre capas
CAPA_TH = 4000          # Umbral de diferencia entre filas para ser la aproximación de una capa
MAX_DIST_PIXELS_TOP = 10# Ventana de movimiento entre píxeles colindantes de un borde hacia arriba
MAX_DIST_PIXELS_BOT = 10# Ventana de movimiento entre píxeles colindantes de un borde hacia abajo
BORDER_SIZE = 10        # Tamaño aproximado del borde completo desde el límite superior al inferior\
SAMPLE_SIZE = 10        # Tamaño ventana para el estudio de las intensidades anteriores y posteriores a un borde
DIST_MIN = 20
N_CAPAS = 3

class ProcessClass(object):

    img = None
    width = None
    height = None
    min_dist_capas = None
    rotation_matrix = None
    mask = None

    def __init__(self, img, rotate_matrix):
        self.img = img
        self.height, self.width, _ = np.shape(img)
        self.min_dist_capas = int(0.1*self.height)
        self.rotation_matrix = rotate_matrix
        self.mask = self._pre_get_masks()

    def _get_nearest_edge(self, edge_image, column, start_position, previous_line):

        for j in range(max(start_position-MAX_DIST_PIXELS_TOP,previous_line),start_position+MAX_DIST_PIXELS_BOT):
            if edge_image[j, column] > 0:
                return j
        return -1

    def _pre_get_masks(self):
        filter_img = cv2.GaussianBlur(self.img, (3, 3), 0)
        _, mask = cv2.threshold(filter_img, 5, 255, cv2.THRESH_BINARY)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((9, 9), np.uint8)
        open_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        kernel = np.ones((11, 11), np.uint8)
        dilated_img = cv2.morphologyEx(open_img, cv2.MORPH_ERODE, kernel)
        return dilated_img

    def _get_edges(self, kernel, canny_values, showEdges=False):

        edge_img = cv2.Canny(self.img, canny_values[0], canny_values[1])
        edge_img = cv2.morphologyEx(edge_img, cv2.MORPH_CLOSE, kernel)

        if showEdges:
            cv2.imshow("Edges", edge_img)
            cv2.waitKey()

        return edge_img

    def _get_starting_pos(self, edge_img, row, previous_line, showStartingPos = False):

        if previous_line != -1:
            has_previous = True
        else:
            has_previous = False

        for i in range(0, self.width):

            #Distancia por encima de la aproximación
            bottom_distance = -1
            for j in range(row,row+DIST_MIN):
                if edge_img[j,i] > 0:
                    if not has_previous or j > previous_line.get_pos("bot", i):
                        bottom_distance = j
                        break
            #Distancia por debajo de la aproximación
            top_distance = -1
            for j in range(row, row-DIST_MIN,-1):
                if edge_img[j,i] > 0:
                    if not has_previous or j > previous_line.get_pos("bot", i):
                        top_distance = j
                        break
            #Si ha encontrado un valor nos quedamos con la columna
            if bottom_distance > -1 or top_distance > -1:
                start_column = i
                if showStartingPos:
                    plt.figure()
                    plt.plot(previous_line)
                    plt.imshow(self.img)
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

    def _get_roi(self,edge_img, showRoi = False):
        # Localizamos lineas de interés
        rows = [sum(edge_img[row, :]) for row in range(0, self.height)]
        diff = [rows[c] - rows[c-1] for c in range(1, len(rows))]
        roi = np.argwhere(np.array(diff) > CAPA_TH)

        previous_result = -1
        result = []
        while 1:
            if previous_result == -1:
                previous_result = int(roi[0])
                result.append(previous_result)
            else:
                try:
                    previous_result = int(roi[roi > previous_result + self.min_dist_capas][0])
                    result.append(previous_result)
                except:
                    break
        if showRoi:
            plt.figure()
            for row in result:
                plt.axhline(y=row)
            plt.imshow(edge_img)
            plt.show()

        return result

    def _rotate_back(self, top_line, bot_line, rotation_matrix):
        M = cv2.invertAffineTransform(rotation_matrix)

        top_line_ones = np.hstack([top_line, np.ones(shape=(len(top_line), 1))])
        bot_line_ones = np.hstack([bot_line, np.ones(shape=(len(bot_line), 1))])


        top_line_inv = M.dot(top_line_ones.T).T
        bot_line_inv = M.dot(bot_line_ones.T).T

        return top_line_inv, bot_line_inv

    def _localization(self, edge_img, showImgs=False):

        height, width = np.shape(edge_img)
        mean = np.mean(self.img)

        #Obtenemos lineas iniciales de aproximación
        rows = self._get_roi(edge_img,showRoi=False)
        N_ROWS = len(rows)

        # Aproximamos las lineas de interés en las diferentes capas
        n_capas = 0
        n_rows = 0

        seg = ImageSegmentationClass()

        while n_capas < N_CAPAS and n_rows < N_ROWS:

            layer = LayerClass(n_capas)
            left_end  = 0
            right_end = self.width

            top_line = [-1] * width
            bot_line = []
            gaps = []
            in_gap = False

            # Encontramos una posición válida para el inicio
            start_value, start_column = self._get_starting_pos(edge_img,rows[n_rows],seg.get_last_bot_line(),showStartingPos=False)

            # Iniciamos la aproximación
            top_line[start_column]  = start_value

            if start_column != -1:

                # Búsqueda por la derecha
                for i in range(start_column+1, width):

                    # Primer borde a partir de la posición anterior
                    pos = self._get_nearest_edge(edge_img, i, top_line[i - 1], seg.get_last_bot_line(i))

                    # En caso de gap
                    if pos == -1:
                        # Mantenemos la misma posición que el punto interior pero evitando cruzar capa anterior
                        pos = max(top_line[i-1], seg.get_last_bot_line(i))
                        # Si estamos en gap y fuera de la imagen
                        if self.mask[pos,i] == 0:
                            if sum(self.mask[pos,i:i+10]) == 0:
                                right_end = i
                                break
                        # Inicializamos variables de control del gap
                        if not in_gap:
                            in_gap = True
                            right_gap = i
                    elif in_gap:
                        gaps.append((right_gap,i)) #Se ha encontrado una posición después de un gap
                        in_gap = False

                    # Almacenamos la posición final
                    top_line[i] = pos

                # Hay demasiado gap --> no es una línea real
                if in_gap  and self.width-right_gap>self.width*0.8:
                    n_rows += 1
                    print("Me salgo por la derecha!")
                    continue

                in_gap = False

                # Búsqueda por la izquierda
                for i in range(start_column-1, -1, -1):

                    # Primer borde a partir de la posición anterior
                    pos = self._get_nearest_edge(edge_img, i, top_line[i + 1], seg.get_last_bot_line(i))

                    # En caso de gap
                    if pos == -1:  # GAP
                        # Mantenemos la misma posición que el punto interior pero evitando cruzar capa anterior
                        pos = max(top_line[i + 1], seg.get_last_bot_line(i))
                        # Si estamos en gap y fuera de la imagen
                        if self.mask[pos,i] == 0:
                            if sum(self.mask[pos,i-10:i]) == 0:
                                left_end = i
                                break
                        # Inicializamos variables de control del gap
                        if not in_gap:
                            in_gap = True
                            left_gap = i
                    elif in_gap:
                        gaps.append((i, left_gap))
                        in_gap = False

                    # Almacenamos la posición final
                    top_line[i] = pos

                if in_gap and left_gap>self.width*0.8:
                    n_rows += 1
                    print("Me salgo por la izquierda!")
                    continue

                layer.set_top_line(top_line[left_end+1:right_end], left_end+1, right_end)
                layer.set_gaps(gaps)
                layer.interpolate_gaps()

                # Comprobamos si es retina
                diff = np.mean([int(np.sum(self.img[(int(top_line[k]) + 10):(int(top_line[k]) + 20), k])) - int(
                    np.sum(self.img[(int(top_line[k]) - 10):int(top_line[k]), k])) for k in range(left_end+1, right_end)])

                print(diff / mean)

                if (diff / mean) > RETINA_TH or n_capas == N_CAPAS-1:
                    n_capas += 1
                    layer.is_retina = True
                    seg.add_layer(layer)
                    break

                # Línea inferior a partir de la superior
                for i in range(0, self.width):
                    aux = [int(edge_img[j, i]) - int(edge_img[j - 1, i]) for j in
                           range(int(top_line[i]), int(top_line[i]) + 30)]
                    bot_line.append(int(np.argmax(np.array(aux[5:]) < 0) + top_line[i] + 5))

                layer.set_bot_line(bot_line[left_end+1:right_end])
                seg.add_layer(layer)

            else:
                print("start_column = -1!")
                n_rows += 1
                plt.figure("Devuelve -1")
                plt.imshow(edge_img)
                for row in rows:
                    plt.axhline(y=row)
                plt.show()
                continue

            n_capas += 1
            n_rows += 1

        if showImgs:
            seg.show(self.img
                     )

        return seg

    def pipeline(self):

        edge_img = self._get_edges(np.ones((5, 5), np.uint8), canny_values=(50, 80), showEdges=False)
        edge_img = cv2.bitwise_or(edge_img, edge_img, mask=self.mask)
        segmentation = self._localization(edge_img, showImgs=True)
        #top_lines, bot_lines = self._rotate_back(top_lines,bot_lines,self.rotation_matrix)

        #return top_lines, bot_lines, n_capas
