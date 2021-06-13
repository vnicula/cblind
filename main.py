import numpy as np
import os
from flask import Flask, render_template, request
from PIL import Image

import img_utils
# from matplotlib.widgets import Slider

app = Flask(__name__)
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['IMAGES_FOLDER'] = os.path.join(APP_ROOT, "static/images")

LMSTD = np.array([[1, 0, 0], [1.10104433,  0, -0.00901975], [0, 0, 1]], dtype=np.float16)
LMSTP = np.array([[0, 0.90822864, 0.008192], [0, 1, 0], [0, 0, 1]], dtype=np.float16)
LMSTT = np.array([[1, 0, 0], [0, 1, 0], [-0.15773032,  1.19465634, 0]], dtype=np.float16)

LMS_GABE1 = np.array([[ 0.58, 0.68, -0.26], [ 0., 1., 0.], [0., 0., 1.]], dtype=np.float16)
LMS_GABE2 = np.array([[ 0.46, 0.62, -0.08], [ 0., 1., 0.], [0., 0., 1.]], dtype=np.float16)
LMS_GABE3 = (LMS_GABE1 + LMS_GABE2) / 2.0
LMS_GABE4 = np.array([[0.81, 0.15, 0.04], [0., 1., 0.], [0., 0., 1.]], dtype=np.float16)
LMS_GABE5 = np.array([[ 0.58, 0.52, -0.1], [ 0., 1., 0.], [0., 0., 1.]], dtype=np.float16)
LMS_GABE6 = np.array([[ 0.7, 0.33, -0.03], [ 0., 1., 0.], [0., 0., 1.]], dtype=np.float16)
LMS_GABE7 = np.array([[ 0.62, 0.53, -0.15], [ 0., 1., 0.], [0., 0., 1.]], dtype=np.float16)

IMG_FRONT = "ishi_3rows.png"
lms_t = LMSTP

def set_lms_sliders_6(lms_t, s1, s2, s3, s4, s5, s6):
  lms_t[0][0] = s1
  lms_t[0][1] = s2
  lms_t[0][2] = 1 - s1 - s2

  lms_t[1][1] = s3
  lms_t[1][0] = s4
  lms_t[1][2] = 1 - s3 - s4

  lms_t[2][2] = s5
  lms_t[2][0] = s6
  lms_t[2][1] = 1 - s5 - s6

  return lms_t

def set_lms_sliders_3(lms_t, s1, s2, s3):
  lms_t[0][0] = 1. - s1
  lms_t[0][1] = 0.90822864 * s1
  lms_t[0][2] = 0.008192 * s1

  lms_t[1][1] = 1. - s2
  lms_t[1][0] = 1.10104433 * s2
  lms_t[1][2] = -0.00901975 * s2

  lms_t[2][2] = 1. - s3
  lms_t[2][0] = -0.15773032 * s3
  lms_t[2][1] = 1.19465634 * s3

  return lms_t


@app.route("/")
def home():
  # user_image = os.path.join(app.config['IMAGES_FOLDER'], 'colorful-cube-pattern_1336x768.jpg')
  # user_image_file_name = 'ishiharatest_1_640.jpeg'
  user_image_file_name = IMG_FRONT
  # user_image_g = os.path.basename(img_utils.rgb2gray(os.path.join(app.config['IMAGES_FOLDER'], user_image)))
  user_image = os.path.join(app.config['IMAGES_FOLDER'], user_image_file_name)
  # user_image_t_file_name = img_utils.process_image(user_image, LMS_GABE3)
  user_image_t_file_name = img_utils.correct_image(user_image)

  return render_template("one_image.html", user_image=user_image_file_name, 
    user_image_g=user_image_t_file_name, min_1=0, max_1=1, min_2=-1.5, max_2=1.5, 
        value1=1, value2=0, value3=1, value4=0, value5=1, value6=0)
  

@app.route("/test", methods=["POST"])
def test():
  if request.method == 'POST':
      print(request.form)
      slider_1 = float(request.form["Slider_1"])
      slider_2 = float(request.form["Slider_2"])
      slider_3 = float(request.form["Slider_3"])
      slider_4 = float(request.form["Slider_4"])
      slider_5 = float(request.form["Slider_5"])
      slider_6 = float(request.form["Slider_6"])
      
  user_image_file_name = IMG_FRONT
  user_image = os.path.join(app.config['IMAGES_FOLDER'], user_image_file_name)

  lms_t = set_lms_sliders_3(lms_t, slider_2, slider_4, slider_6)
  # lms_t = set_lms_sliders_6(lms_t, slider_1, slider_2, slider_3, slider_4, slider_5, slider_6)
  print(lms_t)
  user_image_t_file_name = img_utils.process_image(user_image, lms_t)
  
  return render_template("template.html", user_image=user_image_file_name, 
    user_image_g=user_image_t_file_name, min_1=0, max_1=1, min_2=-1.5, max_2=1.5, value1=slider_1, value2=slider_2, value3=slider_3, value4=slider_4,
    value5=slider_5, value6=slider_6)


@app.route("/view", methods=["POST"])
def view():
  if request.method == 'POST':
      print(request.form)
      slider_1 = float(request.form["Slider_1"])
      slider_2 = float(request.form["Slider_2"])
      slider_3 = float(request.form["Slider_3"])
      slider_4 = float(request.form["Slider_4"])
      slider_5 = float(request.form["Slider_5"])
      slider_6 = float(request.form["Slider_6"])
      
  user_image_file_name = IMG_FRONT
  user_image = os.path.join(app.config['IMAGES_FOLDER'], user_image_file_name)
  lms_t = LMSTD

  lms_t = set_lms_sliders_3(lms_t, slider_1, slider_3, slider_5)
  print(lms_t)
  user_image_t_file_name = img_utils.correct_image(user_image, slider_1, slider_3)

  return render_template("one_image.html", user_image=user_image_file_name, 
    user_image_g=user_image_t_file_name, min_1=0, max_1=1, min_2=-1.5, max_2=1.5, value1=slider_1, value2=slider_2, value3=slider_3, value4=slider_4,
    value5=slider_5, value6=slider_6)


@app.route('/slider_update', methods=['POST'])
def slider():
  received_data = float(request.data)
  print(received_data)
  user_image_file_name = IMG_FRONT
  user_image = os.path.join(app.config['IMAGES_FOLDER'], user_image_file_name)

  user_image_t_file_name = img_utils.correct_image(user_image, received_data, 1.0-lms_t[1][1])
  print(user_image_t_file_name)

  return render_template("one_image.html", user_image=user_image_file_name, 
    user_image_g=user_image_t_file_name, min_1=0, max_1=1, min_2=-1.5, max_2=1.5, value1=received_data, value2=0, value3=0, value4=0,
    value5=0, value6=0)
    

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
