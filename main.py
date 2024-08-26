from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response,flash
import mysql.connector
from functools import wraps
from datetime import datetime, timedelta
import os
import jwt
from models import Model
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import logging

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app=Flask(__name__,template_folder='.')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY']='3d6f45a5fc12445dbac2f59c3b6c7cb1'

model=Model()

db = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    port=int(os.getenv('DB_PORT'))
)
cursor = db.cursor()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    prediction = request.args.get('data', -1)
    is_logged_in = session.get('logged_in', False)
    user = session.get('email', '')
    return render_template("index2.html", data=prediction, is_logged_in=is_logged_in, user=user)


@app.route('/upload',methods=["GET","POST"])
def upload():
    try:
        # if not session.get('logged_in'):  
        #     flash('You must be logged in to upload files.')
        #     return redirect(url_for('home'))
        if request.method=="POST":
            if 'file' not in request.files:
                return redirect(url_for('home'))
            file = request.files['file']
            if file.filename == '':
                return redirect(url_for('home'))
            if file and allowed_file(file.filename):
                # filename = secure_filename(file.filename)
                # file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
                # file.save(file_path)
                try:
                    file_bytes = np.frombuffer(file.read(), np.uint8)
                    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                    model.image_to_feature_vector(image_get=image)
                    pred=model.image_prediction(image=model.image)
                    return redirect(url_for('home',data=pred))
                except Exception as e:
                        logging.error(f"Error processing file: {e}")
                        flash('Error processing file.')
                        return redirect(url_for('home'))
            elif file and not allowed_file(file.filename):
                return redirect(url_for('home'))
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        flash('An unexpected error occurred.')
        return redirect(url_for('home'))

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
    existing_user = cursor.fetchone()
    if existing_user:
        return jsonify({'message': 'User with this username or email already exists!'}), 400

    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                   (username, email, password))
    db.commit()

    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        session['logged_in'] = True
        session['email'] = email
        token = jwt.encode({
            'user': email,
            'exp': datetime.utcnow() + timedelta(seconds=120)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        flash('Login successful!')
        return redirect(url_for('home'))
    else:
        flash('Invalid email or password!')
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
