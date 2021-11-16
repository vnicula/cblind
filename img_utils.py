import numpy as np
import os
from PIL import Image

from lms_utils import Transforms


def add_suffix_to_filename(fpath):
    
    imag_path_dir, imag_name = os.path.split(fpath)
    imag_name, imag_ext = os.path.splitext(imag_name)
    imag_name += '_g' + str(add_suffix_to_filename.img_index)
    add_suffix_to_filename.img_index += 1
    imag_name += imag_ext
    return os.path.join(imag_path_dir, imag_name)

add_suffix_to_filename.img_index = 0


def rgb2gray(rgb_img_path):
    img = Image.open(rgb_img_path)
    imgGray = img.convert('L')
    gray_imag_path = add_suffix_to_filename(rgb_img_path)
    imgGray.save(gray_imag_path)
    return gray_imag_path


def gamma_correction(rgb, gamma=2.4):
    """
    Apply sRGB gamma correction
    :param rgb:
    :param gamma:
    :return: linear_rgb
    """
    linear_rgb = np.zeros_like(rgb, dtype=np.float16)
    for i in range(3):
        idx = rgb[:, :, i] > 0.04045 * 255
        linear_rgb[idx, i] = ((rgb[idx, i] / 255 + 0.055) / 1.055)**gamma
        idx = np.logical_not(idx)
        linear_rgb[idx, i] = rgb[idx, i] / 255 / 12.92
    return linear_rgb


def inverse_gamma_correction(linear_rgb, gamma=2.4):
    """
    :param linear_rgb: array of shape (M, N, 3) with linear sRGB values between in the range [0, 1]
    :param gamma: float
    :return: array of shape (M, N, 3) with inverse gamma correction applied
    """
    rgb = np.zeros_like(linear_rgb, dtype=np.float16)
    for i in range(3):
        idx = linear_rgb[:, :, i] <= 0.0031308
        rgb[idx, i] = 255 * 12.92 * linear_rgb[idx, i]
        idx = np.logical_not(idx)
        rgb[idx, i] = 255 * (1.055 * linear_rgb[idx, i]**(1/gamma) - 0.055)
    return np.round(rgb)


def clip_array(arr, min_value=0, max_value=255):
    """Ensure that all values in an array are between min and max values.
    Arguments:
    ----------
    arr : array_like
    min_value : float, optional
        default 0
    max_value : float, optional
        default 255
    Returns:
    --------
    arr : array_like
        clipped such that all values are min_value <= arr <= max_value
    """
    comp_arr = np.ones_like(arr)
    arr = np.maximum(comp_arr * min_value, arr)
    arr = np.minimum(comp_arr * max_value, arr)
    return arr


def array_to_img(arr, gamma=2.4):
    """Convert a numpy array to a PIL image.
    Arguments:
    ----------
    arr : array of shape (M, N, 3)
    gamma : float exponent of gamma correction
    Returns:
    --------
    img : PIL.Image.Image
        RGB image created from array
    """
    # clip values to lie in the range [0, 255]
    arr = inverse_gamma_correction(arr, gamma=gamma)
    arr = clip_array(arr)
    arr = arr.astype('uint8')
    img = Image.fromarray(arr, mode='RGB')
    return img


def transform_colorspace(img, mat):
    """Transform image to a different color space.
    Arguments:
    ----------
    img : array of shape (M, N, 3)
    mat : array of shape (3, 3)
        conversion matrix to different color space
    Returns:
    --------
    out : array of shape (M, N, 3)
    """
    # Fast element (=pixel) wise matrix multiplication
    return np.einsum("ij, ...j", mat, img, dtype=np.float16, casting="same_kind")


def transform_rgb_with_lms(rgb, lms_t):
    """Transform rgb to lms.
    Arguments:
    ----------
    rgb : array of shape (M, N, 3)
        original image in RGB format
    lms : array of shape (3, 3)
        LMS params
    Returns:
    --------
    rgb_t : array of shape (M, N, 3)
        transformed image in RGB format
    """
    # Colorspace transformation matrices
    cb_matrices = {
        "d": np.array([[1, 0, 0], [1.10104433,  0, -0.00901975], [0, 0, 1]], dtype=np.float16),
        "p": np.array([[0, 0.90822864, 0.008192], [0, 1, 0], [0, 0, 1]], dtype=np.float16),
        "t": np.array([[1, 0, 0], [0, 1, 0], [-0.15773032,  1.19465634, 0]], dtype=np.float16),
    }
    rgb2lms = np.array([[0.3904725 , 0.54990437, 0.00890159],
       [0.07092586, 0.96310739, 0.00135809],
       [0.02314268, 0.12801221, 0.93605194]], dtype=np.float16)
    # Precomputed inverse
    lms2rgb = np.array([[ 2.85831110e+00, -1.62870796e+00, -2.48186967e-02],
       [-2.10434776e-01,  1.15841493e+00,  3.20463334e-04],
       [-4.18895045e-02, -1.18154333e-01,  1.06888657e+00]], dtype=np.float16)
    # first go from RBG to LMS space
    lms = transform_colorspace(rgb, rgb2lms)
    # Calculate image as seen by the color blind
    lms = transform_colorspace(lms, lms_t)
    # Transform back to RBG
    rgb_t = transform_colorspace(lms, lms2rgb)
    return rgb_t


def process_image(user_image, lms_t):
#   user_image = os.path.join(app.config['IMAGES_FOLDER'], user_image)
  orig_img = np.asarray(Image.open(user_image).convert("RGB"), dtype=np.float16)
  orig_img = gamma_correction(orig_img)
  orig_image_g = transform_rgb_with_lms(orig_img, lms_t)
  orig_image_g = array_to_img(orig_image_g)
  user_image_t = add_suffix_to_filename(user_image)
  user_image_t_file_name = os.path.basename(user_image_t)
  orig_image_g.save(user_image_t)

  return user_image_t_file_name


def correct_image(user_image: str,
            protanopia_degree: float = 1.0,
            deutranopia_degree: float = .0,
            return_type: str = 'pil',
            ):
    """
    Use this method to correct images for People with Colorblindness. The images can be corrected for anyone
    having either protanopia, deutranopia, or both. Pass protanopia_degree and deutranopia_degree as diagnosed
    by a doctor using Ishihara test.
    :param input_path: Input path of the image.
    :param protanopia_degree: Protanopia degree as diagnosed by doctor using Ishihara test.
    :param deutranopia_degree: Deutranopia degree as diagnosed by doctor using Ishihara test.
    :param return_type: How to return the Simulated Image. Use 'pil' for PIL.Image, 'np' for Numpy array,
                        'save' for Saving to path.
    :param save_path: Where to save the simulated file. Valid only if return_type is set as 'save'.
    """

    orig_img = np.asarray(Image.open(user_image).convert("RGB"), dtype=np.float16)
    orig_img = gamma_correction(orig_img)

    # img_rgb = Utils.load_rgb(input_path)

    transform = Transforms.correction_matrix(protanopia_degree=protanopia_degree,
                                                deutranopia_degree=deutranopia_degree)
    print(transform)
    # img_corrected = np.uint8(np.dot(img_rgb, transform) * 255)
    # orig_image_g = transform_rgb_with_lms(orig_img, transform.T)
    orig_image_g = np.dot(orig_img, transform)
    orig_image_pil = array_to_img(orig_image_g)
    
    if return_type == 'save':
        user_image_t = add_suffix_to_filename(user_image)
        user_image_t_file_name = os.path.basename(user_image_t)
        orig_image_pil.save(user_image_t)
        return user_image_t_file_name

    if return_type == 'np':
        return orig_image_g

    if return_type == 'pil':
        return orig_image_pil
