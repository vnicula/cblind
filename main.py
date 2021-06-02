import numpy as np
import os
from flask import Flask, render_template, request
from PIL import Image

import img_utils
# from matplotlib.widgets import Slider

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['IMAGES_FOLDER'] = os.path.join(APP_ROOT, "static/images")

LMSTD = np.array([[1, 0, 0], [1.10104433,  0, -0.00901975], [0, 0, 1]], dtype=np.float16)
LMSTP = np.array([[0, 0.90822864, 0.008192], [0, 1, 0], [0, 0, 1]], dtype=np.float16)
LMSTT = np.array([[1, 0, 0], [0, 1, 0], [-0.15773032,  1.19465634, 0]], dtype=np.float16)

LMS_GABE1 = np.array([[ 0.58, 0.68, -0.26], [ 0., 1., 0.], [0., 0., 1.]], dtype=np.float16)
LMS_GABE2 = np.array([[ 0.46, 0.62, -0.08], [ 0., 1., 0.], [0., 0., 1.]], dtype=np.float16)
LMS_GABE3 = (LMS_GABE1 + LMS_GABE2) / 2.0

IMG_FRONT = "colorful-cube-pattern_1336x768.jpg"

@app.route("/")
def home():
  # user_image = os.path.join(app.config['IMAGES_FOLDER'], 'colorful-cube-pattern_1336x768.jpg')
  # user_image_file_name = 'ishiharatest_1_640.jpeg'
  user_image_file_name = IMG_FRONT
  # user_image_g = os.path.basename(img_utils.rgb2gray(os.path.join(app.config['IMAGES_FOLDER'], user_image)))
  user_image = os.path.join(app.config['IMAGES_FOLDER'], user_image_file_name)
  user_image_t_file_name = img_utils.process_image(user_image, LMS_GABE3)

  return render_template("template.html", user_image=user_image_file_name, 
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
  lms_t = LMSTD
  lms_t[0][0] = slider_1
  lms_t[1][1] = slider_3
  lms_t[2][2] = slider_5
  # if slider_1 == 1:
  #   lms_t[0][1] = 0
  #   lms_t[0][2] = 0
  # else:  
  lms_t[0][1] = slider_2
  lms_t[0][2] = 1 - slider_1 - slider_2
  if slider_3 == 1:
    lms_t[1][0] = 0
    lms_t[1][2] = 0
  else:
    lms_t[1][0] = slider_4
    lms_t[1][2] = 1 - slider_4
  if slider_5 == 1:
    lms_t[2][0] = 0
    lms_t[2][1] = 0
  else:
    lms_t[2][0] = slider_6
    lms_t[2][1] = 1 - slider_6
  print(lms_t)
  user_image_t_file_name = img_utils.process_image(user_image, lms_t)
  
  return render_template("template.html", user_image=user_image_file_name, 
    user_image_g=user_image_t_file_name, min_1=0, max_1=1, min_2=-1.5, max_2=1.5, value1=slider_1, value2=slider_2, value3=slider_3, value4=slider_4,
    value5=slider_5, value6=slider_6)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
