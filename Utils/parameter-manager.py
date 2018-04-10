
##############################################PROCCES CLASS#############################################################
RETINA_TH_DEFAULT = 20          # Diferencia de intensidad umbral para ser retina entre los vectores de SAMPLE_SIZE
MIN_DIST_CAPAS_DEFAULT = 20     # Distancia mínima entre capas
CAPA_TH_DEFAULT = 4000          # Umbral de diferencia entre filas para ser la aproximación de una capa
MAX_DIST_PIXELS_TOP_DEFAULT = 10# Ventana de movimiento entre píxeles colindantes de un borde hacia arriba
MAX_DIST_PIXELS_BOT_DEFAULT = 10# Ventana de movimiento entre píxeles colindantes de un borde hacia abajo
BORDER_SIZE_DEFAULT = 10        # Tamaño aproximado del borde completo desde el límite superior al inferior\
SAMPLE_SIZE_DEFAULT = 10        # Tamaño ventana para el estudio de las intensidades anteriores y posteriores a un borde
DIST_MIN_DEFAULT = 20
N_CAPAS_DEFAULT = 3             # Número de capas

#############################################PREPROCCES CLASS###########################################################
MEDIAN_VALUE_DEFAULT = 3
BILATERAL_SIGMA_COLOR_DEFAULT = 150 # Filter sigma in the color space. A larger value of the parameter means that farther
# colors within the pixel neighborhood will be mixed together, resulting in larger areas of semi-equal color.
BILATERAL_SIGMA_SPACE_DEFAULT = 150 # Filter sigma in the coordinate space. A larger value of the parameter means that farther
# pixels will influence each other as long as their colors are close enough (see sigmaColor ).
BILATERAL_DIAMETER_DEFAULT = 11      # Diameter of each pixel neighborhood that is used during filtering.
N_BINS_DEFAULT = 30                  # Bins of orientations to the hog function
ENHANCE_KERNEL_DEFAULT = 15          # Size of the enhance's kernel (n x n)

class ParameterManagerClass(object):

    def __init__(self):
