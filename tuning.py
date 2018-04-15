from Pipeline.process import ProccesClass
from Pipeline.preprocess import PreproccessClass
from Utils.utils import _read_images
from Utils.parameter_manager import ParameterManagerClass

##############################################PROCCES CLASS#############################################################
RETINA_TH_DEFAULT = [23,24,25,26,27,28]         # Diferencia de intensidad umbral para ser retina entre los vectores de SAMPLE_SIZE
MAX_DIST_PIXELS_TOP_DEFAULT = [5,7,10,12,15] # Ventana de movimiento entre píxeles colindantes de un borde hacia arriba
MAX_DIST_PIXELS_BOT_DEFAULT = [5,7,10,12,15] # Ventana de movimiento entre píxeles colindantes de un borde hacia abajo

#############################################PREPROCCES CLASS###########################################################
MEDIAN_VALUE_DEFAULT = [3,5,7,9]
BILATERAL_SIGMA_COLOR_DEFAULT = [100,150,175,200] # Filter sigma in the color space. A larger value of the parameter means that farther
# colors within the pixel neighborhood will be mixed together, resulting in larger areas of semi-equal color.
BILATERAL_SIGMA_SPACE_DEFAULT = [100,150,175,200] # Filter sigma in the coordinate space. A larger value of the parameter means that farther
# pixels will influence each other as long as their colors are close enough (see sigmaColor ).
BILATERAL_DIAMETER_DEFAULT = [7,9,11,13,15]      # Diameter of each pixel neighborhood that is used during filtering.
N_BINS_DEFAULT = [15, 30, 60, 90]                  # Bins of orientations to the hog function
ENHANCE_FUNCTION_DEFAULT = ["top_hat","equalization","adaptative"] # Enhance function

def generate_parameters():
    for retina in RETINA_TH_DEFAULT:
        for dist_top in MAX_DIST_PIXELS_TOP_DEFAULT:
            for disb_bot in MAX_DIST_PIXELS_BOT_DEFAULT:
                for median in MEDIAN_VALUE_DEFAULT:
                    for sigma_color in BILATERAL_SIGMA_COLOR_DEFAULT:
                        for sigma_space in BILATERAL_SIGMA_SPACE_DEFAULT:
                            for diameter in BILATERAL_DIAMETER_DEFAULT:
                                for n_bins in N_BINS_DEFAULT:
                                    for enhance_fuunction in ENHANCE_FUNCTION_DEFAULT:
                                        yield ParameterManagerClass(retina,dist_top,disb_bot,median,sigma_color,
                                                                    sigma_space,diameter,n_bins,enhance_fuunction)



def main():
    image_list, names_list = _read_images()

    for parameters in generate_parameters():

        preprocces = PreproccessClass(parameters)
        procces = ProccesClass(parameters)

        for i in range(0, len(image_list)):
            print(names_list[i])
            rotated_img, enhanced_image, rotation_matrix = preprocces.pipeline(image_list[i])
            result = procces.pipeline(rotated_img, enhanced_image, rotation_matrix)
            result.show(image_list[i])


if __name__ == '__main__':
    main()