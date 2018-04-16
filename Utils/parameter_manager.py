from hashlib import blake2b

##############################################PROCCES CLASS#############################################################
RETINA_TH_DEFAULT = 20          # Diferencia de intensidad umbral para ser retina entre los vectores de SAMPLE_SIZE
MAX_DIST_PIXELS_TOP_DEFAULT = 10# Ventana de movimiento entre píxeles colindantes de un borde hacia arriba
MAX_DIST_PIXELS_BOT_DEFAULT = 10# Ventana de movimiento entre píxeles colindantes de un borde hacia abajo

#############################################PREPROCCES CLASS###########################################################
MEDIAN_VALUE_DEFAULT = 3
BILATERAL_SIGMA_COLOR_DEFAULT = 150 # Filter sigma in the color space. A larger value of the parameter means that farther
# colors within the pixel neighborhood will be mixed together, resulting in larger areas of semi-equal color.
BILATERAL_SIGMA_SPACE_DEFAULT = 150 # Filter sigma in the coordinate space. A larger value of the parameter means that farther
# pixels will influence each other as long as their colors are close enough (see sigmaColor ).
BILATERAL_DIAMETER_DEFAULT = 11      # Diameter of each pixel neighborhood that is used during filtering.
N_BINS_DEFAULT = 30                  # Bins of orientations to the hog function
ENHANCE_FUNCTION_DEFAULT = "top_hat" # Enhance function

class ParameterManagerClass(object):

    id = None
    retina_th = RETINA_TH_DEFAULT
    max_dist_top = MAX_DIST_PIXELS_TOP_DEFAULT
    max_dist_bot = MAX_DIST_PIXELS_BOT_DEFAULT
    median_value = MEDIAN_VALUE_DEFAULT
    sigma_color = BILATERAL_SIGMA_COLOR_DEFAULT
    sigma_space = BILATERAL_SIGMA_SPACE_DEFAULT
    bilateral_diameter = BILATERAL_DIAMETER_DEFAULT
    n_bins = N_BINS_DEFAULT
    enhance_function = ENHANCE_FUNCTION_DEFAULT


    def __init__(self, retina_th = None, max_dist_top = None, max_dist_bot = None, median_value = None, sigma_color = None,
                 sigma_space = None, bilateral_diameter = None, n_bins = None, enhance_function = None):

        if retina_th:
            self.retina_th = retina_th
        if max_dist_top:
            self.max_dist_top = max_dist_top
        if max_dist_bot:
            self.max_dist_bot = max_dist_bot
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
        if enhance_function:
            self.enhance_function = enhance_function


        h = blake2b(digest_size=20)
        config_id = str(self.get_config()).encode('utf-8')
        h.update(config_id)
        self.id = h.hexdigest()


    def get_config(self):
        return {
            "RETINA_TH": self.retina_th,
            "MAX_DIST_TOP": self.max_dist_top,
            "MAX_DIST_BOT": self.max_dist_bot,
            "MEDIAN_VALUE": self.median_value,
            "SIGMA_COLOR": self.sigma_color,
            "SIGMA_SPACE": self.sigma_space,
            "BILATERAL_DIAMETER": self.bilateral_diameter,
            "N_BINS": self.n_bins,
            "ENHANCE_KERNEL": self.enhance_function
        }