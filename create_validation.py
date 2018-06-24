from Validation.validate_data import ValidateData
from Utils import utils

def main():
    ValidateData().create_validation()
    #image_list,  names_list = utils._read_images()
    #utils.show_validations(names_list,image_list)
        
if __name__ == '__main__':
    main()