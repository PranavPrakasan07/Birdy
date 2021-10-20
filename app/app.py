import os
from flask import Flask,render_template,request,flash,redirect,url_for
from keras_preprocessing import image
from werkzeug.utils import secure_filename
import numpy as np
UPLOAD_FOLDER="/Users/ramkrithik/Desktop/HCI/project/upload/"
from tensorflow.keras.models import load_model
import tensorflow.keras.utils as image
import names


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "1234"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
@app.route("/home")
def first():
    return render_template("index.html")

@app.route("/upload")
def upload():
    return render_template("second.html")
    
@app.route("/process",methods=["POST", "GET"])
def third():
    if request.method == 'POST':
        f = request.files['fileToUpload']
        print("current path")
        basepath = os.path.dirname(__file__)
        print("current path", basepath)
        s=secure_filename(f.filename)
        filepath = os.path.join(basepath,'upload',s)
        print("upload folder is ", filepath)
        f.save(filepath)
        return redirect(url_for("model",name=s))
    #return render_template("third.html")

@app.route("/display/<name>")
def model(name):
    x=UPLOAD_FOLDER+name
    model = load_model("/Users/ramkrithik/Desktop/HCI/project/birdModel.h5")
    img = image.load_img(x,target_size = (64,64))
    x = image.img_to_array(img)
    x = np.expand_dims(x,axis =0)
    preds = model.predict(x)

    prediction = names.name(int(preds[0][0]))
    print(preds)
    print("prediction", prediction)
        
    text = "The prediction is : " + str(prediction)
        
    return text
    #return x
    #return render_template("third.html")

@app.route("/fourth")
def fourth():
    return render_template("fourth.html")

if __name__ == '__main__':
    app.run(debug=True)
