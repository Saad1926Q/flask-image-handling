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
    return render_template("index.html")

@app.route('/upload',methods=["GET","POST"])
def upload():
    if request.method=="POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template("index.html")
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('home'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # return redirect(url_for('download_file', name=filename))
            model.image_to_feature_vector(image_path=file_path)
            pred=model.image_prediction(image=model.image)
            flash(pred)
            return render_template("index.html") 
        elif file and not allowed_file(file.filename):
            flash('Incorrect Format')
            return render_template("index.html")


app.run(debug=True)