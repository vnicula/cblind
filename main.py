import os
from flask import Flask, render_template

import img_utils

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['IMAGES_FOLDER'] = os.path.join(APP_ROOT, "static/images")


@app.route("/")
def home():
  # user_image = os.path.join(app.config['IMAGES_FOLDER'], 'colorful-cube-pattern_1336x768.jpg')
  user_image = 'colorful-cube-pattern_1336x768.jpg'
  user_image_g = os.path.basename(img_utils.rgb2gray(os.path.join(app.config['IMAGES_FOLDER'], user_image)))
  return render_template("template.html", user_image=user_image, user_image_g=user_image_g)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
