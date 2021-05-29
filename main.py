import numpy as np
import os
from flask import Flask, render_template, request
from PIL import Image

import img_utils

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['IMAGES_FOLDER'] = os.path.join(APP_ROOT, "static/images")

LMST = np.array([[0, 0.90822864, 0.008192], [0, 1, 0], [0, 0, 1]], dtype=np.float16)

@app.route("/")
def home():
  # user_image = os.path.join(app.config['IMAGES_FOLDER'], 'colorful-cube-pattern_1336x768.jpg')
  user_image = 'ishiharatest_1_640.jpeg'
  # user_image_g = os.path.basename(img_utils.rgb2gray(os.path.join(app.config['IMAGES_FOLDER'], user_image)))
  user_image = os.path.join(app.config['IMAGES_FOLDER'], user_image)
  orig_img = np.asarray(Image.open(user_image).convert("RGB"), dtype=np.float16)
  orig_img = img_utils.gamma_correction(orig_img)
  orig_image_g = img_utils.transform_rgb_with_lms(orig_img, LMST)
  orig_image_g = img_utils.array_to_img(orig_image_g)
  user_image_t = img_utils.add_suffix_to_filename(user_image)
  save_path_user_image_t = os.path.basename(user_image_t)
  orig_image_g.save(user_image_t)
  return render_template("template.html", user_image=os.path.basename(user_image), 
    user_image_g=save_path_user_image_t, min_1 = -1, max_1 = 1)
  
@app.route("/test", methods=["POST"])
def test():
    name_of_slider = "A"
    if request.method == 'POST':
        name_of_slider = request.form["Slider_1"]
        # min_of_slider = request.form["min_1"]
    print(request.form["Slider_1"])
    return name_of_slider

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
