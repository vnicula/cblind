import numpy as np
import os
from flask import Flask, render_template, request
from PIL import Image

import img_utils

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['IMAGES_FOLDER'] = os.path.join(APP_ROOT, "static/images")

LMSTD = np.array([[1, 0, 0], [1.10104433,  0, -0.00901975], [0, 0, 1]], dtype=np.float16)
LMSTP = np.array([[0, 0.90822864, 0.008192], [0, 1, 0], [0, 0, 1]], dtype=np.float16)
LMSTT = np.array([[1, 0, 0], [0, 1, 0], [-0.15773032,  1.19465634, 0]], dtype=np.float16)

@app.route("/")
def home():
  # user_image = os.path.join(app.config['IMAGES_FOLDER'], 'colorful-cube-pattern_1336x768.jpg')
  user_image_file_name = 'ishiharatest_1_640.jpeg'
  # user_image_file_name = 'color_wheel_640.png'
  # user_image_g = os.path.basename(img_utils.rgb2gray(os.path.join(app.config['IMAGES_FOLDER'], user_image)))
  user_image = os.path.join(app.config['IMAGES_FOLDER'], user_image_file_name)
  user_image_t_file_name = img_utils.process_image(user_image, LMSTT)

  return render_template("template.html", user_image=user_image_file_name, 
    user_image_g=user_image_t_file_name, min_1=0, max_1=1, min_2=-1.25, max_2=1.25)
  

@app.route("/test", methods=["POST"])
def test():
  if request.method == 'POST':
      slider_1 = float(request.form["Slider_1"])
      slider_2 = float(request.form["Slider_2"])
      slider_3 = float(request.form["Slider_3"])
      slider_4 = float(request.form["Slider_4"])
  user_image_file_name = 'ishiharatest_1_640.jpeg'
  user_image = os.path.join(app.config['IMAGES_FOLDER'], user_image_file_name)
  lms_t = LMSTD
  lms_t[0][0] = slider_1
  lms_t[1][1] = slider_3
  if slider_1 == 1:
    lms_t[0][1] = 0
    lms_t[0][2] = 0
  else:
    lms_t[0][1] = slider_2
    lms_t[0][2] = 1 - slider_2
  if slider_3 == 1:
    lms_t[1][0] = 0
    lms_t[1][2] = 0
  else:
    lms_t[1][0] = slider_4
    lms_t[1][2] = 1 - slider_4
  print(lms_t)
  user_image_t_file_name = img_utils.process_image(user_image, lms_t)
  
  return render_template("template.html", user_image=user_image_file_name, 
    user_image_g=user_image_t_file_name, min_1=0, max_1=1, min_2=-1.5, max_2=1.5)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
