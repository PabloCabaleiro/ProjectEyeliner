from hashlib import blake2b

##############################################PROCCES CLASS#############################################################
#Detección de ROI
CORNEA_TH_DEFAULT = 30               # Diferencia de intensidad umbral para ser cornea entre los vectores de SAMPLE_SIZE
MAX_DIST_TO_ROI_DEFAULT = 20         # Distancia máxima a la línea marcada como ROI para ser punto de inicio
#Aproximación al borde
LOCALIZATION_TOP_WINDOW_DEFAULT = 10 # Ventana de movimiento entre píxeles colindantes de un borde hacia arriba
LOCALIZATION_BOT_WINDOW_DEFAULT = 10 # Ventana de movimiento entre píxeles colindantes de un borde hacia abajo
#Detección de capas
MIN_DIST_BETWEEN_ROI_RATE = 0.05          # Distancia mínima entre capas
ROI_TH_DEFAULT = 3000                # Umbral de diferencia entre filas para ser la aproximación de una capa
EDGE_WIDTH_DEFAULT = 10              # Tamaño aproximado del borde completo desde el límite superior al inferior\
SAMPLE_WINDOW_DEFAULT = 10           # Tamaño ventana para el estudio de las intensidades anteriores y posteriores a un borde
N_ROI_DEFAULT = 3
#Snake
BETA_DEFAULT = 20                    # Snake length shape parameter. Higher values makes snake contract faster.
ALPHA_DEFAULT = 50                   # Snake smoothness shape parameter. Higher values makes snake smoother.
W_LINE_DEFAULT = 0                   # Controls attraction to brightness. Use negative values to attract to dark regions.
W_EDGE_DEFAULT = 1                   # Controls attraction to edges. Use negative values to repel snake from edges
GAMMA_DEFAULT = 0.1                  # Explicit time stepping parameter.
#Canny
CANNY_SUP_DEFAULT = 60
CANNY_INF_DEFAULT = 40
CANNY_KERNER_DEFAULT = 5

#############################################PREPROCCES CLASS###########################################################
MEDIAN_VALUE_DEFAULT = 3
BILATERAL_SIGMA_COLOR_DEFAULT = 150 # Filter sigma in the color space. A larger value of the parameter means that farther
# colors within the pixel neighborhood will be mixed together, resulting in larger areas of semi-equal color.
BILATERAL_SIGMA_SPACE_DEFAULT = 150 # Filter sigma in the coordinate space. A larger value of the parameter means that farther
# pixels will influence each other as long as their colors are close enough (see sigmaColor ).
BILATERAL_DIAMETER_DEFAULT = 11      # Diameter of each pixel neighborhood that is used during filtering.
N_BINS_DEFAULT = 30                  # Bins of orientations to the hog function
TOP_HAT_KERNEL_SIZE = 15

class ParameterManagerClass(object):

    id = None
    min_dist_between_roi = MIN_DIST_BETWEEN_ROI_RATE
    roi_th = ROI_TH_DEFAULT
    cornea_th = CORNEA_TH_DEFAULT
    max_dist_to_roi = MAX_DIST_TO_ROI_DEFAULT
    edge_width = EDGE_WIDTH_DEFAULT
    sample_window = SAMPLE_WINDOW_DEFAULT
    localization_top_window = LOCALIZATION_TOP_WINDOW_DEFAULT
    localization_bot_window = LOCALIZATION_BOT_WINDOW_DEFAULT
    median_value = MEDIAN_VALUE_DEFAULT
    sigma_color = BILATERAL_SIGMA_COLOR_DEFAULT
    sigma_space = BILATERAL_SIGMA_SPACE_DEFAULT
    bilateral_diameter = BILATERAL_DIAMETER_DEFAULT
    n_bins = N_BINS_DEFAULT
    n_roi = N_ROI_DEFAULT
    beta = BETA_DEFAULT
    alpha = ALPHA_DEFAULT
    w_line = W_LINE_DEFAULT
    w_edge = W_EDGE_DEFAULT
    gamma = GAMMA_DEFAULT
    canny_sup = CANNY_SUP_DEFAULT
    canny_inf = CANNY_INF_DEFAULT
    canny_kernel = CANNY_KERNER_DEFAULT
    top_hat_kernel = TOP_HAT_KERNEL_SIZE

    def __init__(self, max_dist_top = None, max_dist_bot = None, median_value = None, sigma_color = None,
                 sigma_space = None, bilateral_diameter = None, n_bins = None, min_dist_roi = None,
                 roi_th = None, cornea_th = None, border_size = None, max_dist_to_roi = None, n_roi = None, sample_size= None,
                 alpha = None, beta = None, w_line = None, w_edge = None, gamma = None, canny_sup = None, canny_inf = None,
                 canny_kernel = None, top_hat_kernel = None):

        if top_hat_kernel:
            self.top_hat_kernel = top_hat_kernel
        if canny_inf:
            self.canny_inf = canny_inf
        if canny_sup:
            self.canny_sup = canny_sup
        if canny_kernel:
            self.canny_kernel = canny_kernel
        if max_dist_top:
            self.localization_top_window = max_dist_top
        if max_dist_bot:
            self.localization_bot_window = max_dist_bot
        if median_value:
            self.median_value = median_value
        if sigma_color:
            self.sigma_color = sigma_color
        if sigma_space:
            self.sigma_space = sigma_space
        if bilateral_diameter:
            self.bilateral_diameter = bilateral_diameter
        if n_bins:
            self.n_bins = n_bins
        if min_dist_roi:
            self.min_dist_between_roi = min_dist_roi
        if roi_th:
            self.roi_th = roi_th
        if cornea_th:
            self.cornea_th = cornea_th
        if border_size:
            self.edge_width = border_size
        if max_dist_to_roi:
            self.max_dist_to_roi = max_dist_to_roi
        if n_roi:
            self.n_roi = n_roi
        if alpha:
            self.alpha = alpha
        if beta:
            self.beta = beta
        if w_edge:
            self.w_edge = w_edge
        if w_line:
            self.w_line = w_line
        if gamma:
            self.gamma = gamma
        if sample_size:
            self.sample_window = sample_size

        h = blake2b(digest_size=20)
        config_id = str(self.get_config()).encode('utf-8')
        h.update(config_id)
        self.id = h.hexdigest()


    def get_config(self):
        return {
            "ID": self.id,
            "CORNEA_TH": self.cornea_th,
            "MEDIAN_VALUE": self.median_value,
            "SIGMA_COLOR": self.sigma_color,
            "SIGMA_SPACE": self.sigma_space,
            "BILATERAL_DIAMETER": self.bilateral_diameter,
            "ALPHA": self.alpha,
            "BETA": self.beta,
            "W_LINE": self.w_line,
            "W_EDGE": self.w_edge,
            "GAMMA": self.gamma,
            "CANNY_SUP": self.canny_sup,
            "CANNY_INF": self.canny_inf,
            "CANNY_KERNEL": self.canny_kernel,
            "TOP_HAT_KERNEL": self.top_hat_kernel,
        }