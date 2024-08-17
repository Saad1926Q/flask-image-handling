from flask import Flask,render_template,request,flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app=Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY']='3d6f45a5fc12445dbac2f59c3b6c7cb1'

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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('download_file', name=filename))
            return render_template("index.html") 
        elif file and not allowed_file(file.filename):
            flash('Incorrect Format')
            return render_template("index.html")


app.run(debug=True)