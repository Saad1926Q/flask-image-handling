from flask import Flask,render_template,request,flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

from models import Model

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app=Flask(__name__,template_folder='.')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY']='3d6f45a5fc12445dbac2f59c3b6c7cb1'

model=Model()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    prediction = request.args.get('data',-1)
    return render_template("index2.html",data=prediction)


@app.route('/upload',methods=["GET","POST"])
def upload():
    if request.method=="POST":
        if 'file' not in request.files:
            return redirect(url_for('home'))
        file = request.files['file']
        if file.filename == '':
            return redirect(url_for('home'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            model.image_to_feature_vector(image_path=file_path)
            pred=model.image_prediction(image=model.image)
            return redirect(url_for('home',data=pred))
        elif file and not allowed_file(file.filename):
            return redirect(url_for('home'))


app.run(debug=True)