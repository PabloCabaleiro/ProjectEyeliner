import cv2
import numpy as np
import matplotlib.pyplot as plt

RETINA_TH = 20          # Diferencia de intensidad umbral para ser retina entre los vectores de SAMPLE_SIZE
MIN_DIST_CAPAS = 20     # Distancia mínima entre capas
N_CAPAS = 3             # Número de capas
CAPA_TH = 5000          # Umbral de diferencia entre filas para ser la aproximación de una capa
MAX_DIST_PIXELS_TOP = 20# Ventana de movimiento entre píxeles colindantes de un borde hacia arriba
MAX_DIST_PIXELS_BOT = 20# Ventana de movimiento entre píxeles colindantes de un borde hacia abajo
BORDER_SIZE = 10        # Tamaño aproximado del borde completo desde el límite superior al inferior\
SAMPLE_SIZE = 10        # Tamaño ventana para el estudio de las intensidades anteriores y posteriores a un borde
DIST_MIN = 20

class ProccessClass(object):

    img = None
    width = None
    height = None

    def __init__(self, img):
        self.img = img
        self.height, self.width, _ = np.shape(img)

    def _get_nearest_edge(self, edge_image, column, start_position, previous_line):

        if len(previous_line) == 0:
            for j in range(start_position-MAX_DIST_PIXELS_TOP, start_position+MAX_DIST_PIXELS_BOT):
                if edge_image[j, column] > 0:
                    return j
        else:
            for j in range(max(start_position-MAX_DIST_PIXELS_TOP,previous_line[column]),start_position+MAX_DIST_PIXELS_BOT):
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

        if previous_line != []:
            has_previous = True
        else:
            has_previous = False


        for i in range(0, self.width):

            #Distancia por encima de la aproximación
            bottom_distance = -1
            for j in range(row,row+DIST_MIN):
                if edge_img[j,i] > 0:
                    if not has_previous or j > previous_line[i] + MIN_DIST_CAPAS:
                        bottom_distance = j
                        break
            #Distancia por debajo de la aproximación
            top_distance = -1
            for j in range(row, row-DIST_MIN,-1):
                if edge_img[j,i] > 0:
                    if not has_previous or j > previous_line[i] + MIN_DIST_CAPAS:
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
                if (row - top_distance > bottom_distance - row):
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
        diff = [rows[c + 1] - rows[c] for c in range(0, len(rows) - 1)]
        roi = np.argwhere(np.array(diff) > CAPA_TH)

        row1 = int(roi[0])
        row2 = int(roi[roi > row1 + MIN_DIST_CAPAS][0])
        row3 = int(roi[roi > row2 + MIN_DIST_CAPAS][0])

        if showRoi:
            plt.figure()
            for row in [row1, row2, row3]:
                plt.axhline(y=row)
            plt.imshow(edge_img)
            plt.show()

        return [row1, row2, row3]

    def rotate_back(image, rotation_matrix, og_size):
        M = cv2.invertAffineTransform(rotation_matrix)
        return cv2.warpAffine(image, M, (og_size[1], og_size[0]))

    def _localization(self, edge_img, showImgs=False):

        height, width = np.shape(edge_img)
        mean = np.mean(self.img)

        #Obtenemos lineas iniciales de aproximación
        rows = self._get_roi(edge_img,showRoi=False)

        # Aproximamos las lineas de interés en las diferentes capas
        c = 0
        top_lines = []
        bot_lines = []
        columns = []

        while c < N_CAPAS:
            line_a = [None] * width
            line_b = []
            gaps = []
            in_gap = False
            start_gap = -1

            # Encontramos una posición válida para el inicio
            if c == 0:
                start_value, start_column = self._get_starting_pos(edge_img,rows[c],[],showStartingPos=False)
            else:
                start_value, start_column = self._get_starting_pos(edge_img,rows[c],bot_lines[c-1],showStartingPos=False)

            columns.append(start_column)

            line_a[start_column]  = start_value

            if start_column != -1:
                # Búsqueda por la derecha
                for i in range(start_column+1, width):

                    # Primer borde a partir de la posición anterior
                    if c == 0:
                        pos = self._get_nearest_edge(edge_img, i, line_a[i - 1], [])
                    else:
                        pos = self._get_nearest_edge(edge_img, i, line_a[i - 1], bot_lines[c-1])

                    # Procesar esta linea (agujeros...)
                    if pos == -1: #GAP
                        pos = line_a[i-1]
                        if not in_gap:
                            in_gap = True
                            start_gap = i
                    elif in_gap:
                        gaps.append((start_gap,i))
                        in_gap = False

                    # Almacenamos la posición final
                    line_a[i] = pos

                in_gap = False

                # Búsqueda por la izquierda
                for i in range(start_column-1, -1, -1):

                    # Primer borde a partir de la posición anterior
                    if c == 0:
                        pos = self._get_nearest_edge(edge_img, i, line_a[i + 1], [])
                    else:
                        pos = self._get_nearest_edge(edge_img, i, line_a[i + 1], bot_lines[c-1])

                    # Procesar esta linea (agujeros...)
                    if pos == -1:  # GAP
                        pos = line_a[i + 1]
                        if not in_gap:
                            in_gap = True
                            start_gap = i
                    elif in_gap:
                        gaps.append((i, start_gap))
                        in_gap = False

                    # Almacenamos la posición final
                    line_a[i] = pos

                #Interpolamos los gaps
                for start, end in gaps:
                    step = (line_a[end] - line_a[start]) / (end - start)
                    for k in range(start, end):
                        line_a[k] = round(line_a[k - 1] + step)

                top_lines.append(line_a)

                # Comprobamos si es retina
                diff = np.mean([int(np.sum(self.img[(int(line_a[k]) + 10):(int(line_a[k]) + 20), k])) - int(
                    np.sum(self.img[(int(line_a[k]) - 10):int(line_a[k]), k])) for k in range(0, width)])

                if diff / mean > RETINA_TH:
                    break

                # Línea inferior a partir de la superior
                for i in range(0, width):
                    aux = [int(edge_img[j, i]) - int(edge_img[j - 1, i]) for j in
                           range(int(line_a[i]), int(line_a[i]) + 30)]
                    line_b.append(int(np.argmax(np.array(aux[5:]) < 0) + line_a[i] + 5))

                bot_lines.append(line_b)

            else:
                break

            c += 1

        plt.imshow(self.img)
        for line in top_lines:
            plt.plot(line)
        for line in bot_lines:
            plt.plot(line)
        #for row in rows:
        #    plt.axhline(y=row)
        #for col in columns:
        #    plt.axvline(x=col)
        plt.title(str(c))
        plt.show()

    def pipeline(self):

        mask = self._pre_get_masks()
        edge_img = self._get_edges(np.ones((5, 5), np.uint8), canny_values=(50, 80), showEdges=False)
        edge_img = cv2.bitwise_or(edge_img, edge_img, mask=mask)
        return self._localization(edge_img, showImgs=True)