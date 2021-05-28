import os
from PIL import Image

def rgb2gray(rgb_img_path):
    img = Image.open(rgb_img_path)
    imgGray = img.convert('L')
    gray_imag_path_dir, gray_imag_name = os.path.split(rgb_img_path)
    gray_imag_name, gray_imag_ext = os.path.splitext(gray_imag_name)
    gray_imag_name += '_g'
    gray_imag_name += gray_imag_ext
    gray_imag_path = os.path.join(gray_imag_path_dir, gray_imag_name)
    imgGray.save(gray_imag_path)
    return gray_imag_path