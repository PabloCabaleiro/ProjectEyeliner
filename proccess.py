import cv2
import numpy as np
import matplotlib.pyplot as plt

RETINA_TH = 27          # Diferencia de intensidad umbral para ser retina entre los vectores de SAMPLE_SIZE
MIN_DIST_CAPAS = 30     # Distancia mínima entre capas
CAPA_TH = 4000          # Umbral de diferencia entre filas para ser la aproximación de una capa
MAX_DIST_PIXELS_TOP = 20# Ventana de movimiento entre píxeles colindantes de un borde hacia arriba
MAX_DIST_PIXELS_BOT = 20# Ventana de movimiento entre píxeles colindantes de un borde hacia abajo
BORDER_SIZE = 10        # Tamaño aproximado del borde completo desde el límite superior al inferior\
SAMPLE_SIZE = 10        # Tamaño ventana para el estudio de las intensidades anteriores y posteriores a un borde
DIST_MIN = 20
N_CAPAS = 3

class ProccessClass(object):

    img = None
    width = None
    height = None
    min_dist_capas = None

    def __init__(self, img):
        self.img = img
        self.height, self.width, _ = np.shape(img)
        self.min_dist_capas = int(0.1*self.height)

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
                    if not has_previous or j > previous_line[i] + self.min_dist_capas:
                        bottom_distance = j
                        break
            #Distancia por debajo de la aproximación
            top_distance = -1
            for j in range(row, row-DIST_MIN,-1):
                if edge_img[j,i] > 0:
                    if not has_previous or j > previous_line[i] + self.min_dist_capas:
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

    def rotate_back(image, rotation_matrix, og_size):
        M = cv2.invertAffineTransform(rotation_matrix)
        return cv2.warpAffine(image, M, (og_size[1], og_size[0]))

    def _localization(self, edge_img, showImgs=False):

        height, width = np.shape(edge_img)
        mean = np.mean(self.img)

        #Obtenemos lineas iniciales de aproximación
        rows = self._get_roi(edge_img,showRoi=False)
        N_ROWS = len(rows)

        # Aproximamos las lineas de interés en las diferentes capas
        n_capas = 0
        top_lines = []
        bot_lines = []
        n_rows = 0

        while n_capas < N_CAPAS and n_rows < N_ROWS:
            line_a = [None] * width
            line_b = []
            gaps = []
            in_gap = False

            # Encontramos una posición válida para el inicio
            if n_capas == 0:
                start_value, start_column = self._get_starting_pos(edge_img,rows[n_rows],[],showStartingPos=False)
            else:
                start_value, start_column = self._get_starting_pos(edge_img,rows[n_rows],bot_lines[-1],showStartingPos=False)

            line_a[start_column]  = start_value

            if start_column != -1:
                # Búsqueda por la derecha
                for i in range(start_column+1, width):

                    # Primer borde a partir de la posición anterior
                    if n_capas == 0:
                        pos = self._get_nearest_edge(edge_img, i, line_a[i - 1], [])
                    else:
                        pos = self._get_nearest_edge(edge_img, i, line_a[i - 1], bot_lines[-1])

                    # Procesar esta linea (agujeros...)
                    if pos == -1: #GAP
                        if n_capas == 0:
                            pos = line_a[i-1]
                        else:
                            pos = max(line_a[i-1], bot_lines[-1][i] + self.min_dist_capas)
                        if not in_gap:
                            in_gap = True
                            right_gap = i
                    elif in_gap:
                        gaps.append((right_gap,i))
                        in_gap = False

                    # Almacenamos la posición final
                    line_a[i] = pos

                # Hay demasiado gap --> no es una línea real
                if in_gap  and self.width-right_gap>self.width/2:
                    n_rows += 1
                    print("Me salgo por la derecha!")
                    continue

                in_gap = False

                # Búsqueda por la izquierda
                for i in range(start_column-1, -1, -1):

                    # Primer borde a partir de la posición anterior
                    if n_capas == 0:
                        pos = self._get_nearest_edge(edge_img, i, line_a[i + 1], [])
                    else:
                        pos = self._get_nearest_edge(edge_img, i, line_a[i + 1], bot_lines[-1])

                    # Procesar esta linea (agujeros...)
                    if pos == -1:  # GAP
                        if n_capas == 0:
                            pos = line_a[i + 1]
                        else:
                            pos = max(line_a[i + 1], bot_lines[-1][i] + self.min_dist_capas)
                        if not in_gap:
                            in_gap = True
                            left_gap = i
                    elif in_gap:
                        gaps.append((i, left_gap))
                        in_gap = False

                    # Almacenamos la posición final
                    line_a[i] = pos

                if in_gap and left_gap>self.width/2:
                    n_rows += 1
                    print("Me salgo por la izquierda!")
                    continue

                #Interpolamos los gaps
                for start, end in gaps:
                    step = (line_a[end] - line_a[start]) / (end - start)
                    for k in range(start, end):
                        line_a[k] = round(line_a[k - 1] + step)

                top_lines.append(line_a)

                # Comprobamos si es retina
                diff = np.mean([int(np.sum(self.img[(int(line_a[k]) + 10):(int(line_a[k]) + 20), k])) - int(
                    np.sum(self.img[(int(line_a[k]) - 10):int(line_a[k]), k])) for k in range(left_gap, right_gap)])

                if (diff / mean) > RETINA_TH or n_capas == N_CAPAS-1:
                    print(diff/mean)
                    break

                # Línea inferior a partir de la superior
                for i in range(0, width):
                    aux = [int(edge_img[j, i]) - int(edge_img[j - 1, i]) for j in
                           range(int(line_a[i]), int(line_a[i]) + 30)]
                    line_b.append(int(np.argmax(np.array(aux[5:]) < 0) + line_a[i] + 5))

                bot_lines.append(line_b)

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

        plt.imshow(self.img)
        for line in top_lines:
            plt.plot(line)
        for line in bot_lines:
            plt.plot(line)
        #for row in rows:
        #    plt.axhline(y=row)
        plt.title(str(n_capas))
        plt.show()

    def pipeline(self):

        mask = self._pre_get_masks()
        edge_img = self._get_edges(np.ones((5, 5), np.uint8), canny_values=(50, 80), showEdges=False)
        edge_img = cv2.bitwise_or(edge_img, edge_img, mask=mask)
        return self._localization(edge_img, showImgs=True)