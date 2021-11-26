# .....................................PACKAGES
import os
from flask import Flask, render_template, request, flash, redirect, url_for
from keras_preprocessing import image
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow.keras.utils as image
import names

# ....................................INITIALISATION
UPLOAD_FOLDER = "app/uploads/upload/"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "1234"

# ....................................HOME


@app.route("/")
@app.route("/home")
def first():
    print("Home")
    return render_template("index.html")

# ....................................UPLOAD


@app.route("/upload")
def upload():
    print("Upload")
    return render_template("upload.html")

# .....................................FILE HANDLING


@app.route("/process", methods=["POST", "GET"])
def third():
    print("Process")
    if request.method == 'POST':
        f = request.files['fileToUpload']
        print("current path")
        basepath = os.path.dirname(__file__)
        print("current path", basepath)
        s = secure_filename(f.filename)
        filepath = os.path.join(basepath, 'upload', s)
        print("upload folder is ", filepath)
        f.save(filepath)
        return redirect(url_for("model", name=s))

# ......................................PREDICTION


@app.route("/display/<name>")
def model(name):
    x = UPLOAD_FOLDER+name
    model = load_model("birdModel.h5")
    img = image.load_img(x, target_size=(64, 64))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    preds = list(model.predict(x))
    for i, j in enumerate(preds):
        preds[i] = list(j)
    prediction = names.name(preds[0].index(max(preds[0])))
    before = prediction
    print("prediction", prediction)
    if " " in prediction:
        prediction = prediction.split(" ")
        prediction[0] = prediction[0].capitalize()
        for i in range(1, len(prediction)):
            prediction[i] = prediction[i].lower()
        prediction = "_".join(prediction)
    else:
        prediction = prediction.capitalize()
    text = "The prediction is : " + prediction
    return render_template("facts.html", name=before)

# .......................................UPDATES


@app.route("/new")
def fourth():
    return render_template("fourth.html")


if __name__ == '__main__':
    app.run(debug=True)
