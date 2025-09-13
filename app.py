import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'a_very_secret_key'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/pdf', methods=['GET', 'POST'])
def upload_pdf():
    if request.method == "POST":
        print("pdf")
    return render_template("pdf-upload.html")

@app.route('/image', methods=['GET', 'POST'])
def upload_img():
    if request.method == "POST":
        print("image")
    return render_template("image-upload.html")

@app.route('/text', methods=['GET', 'POST'])
def upload_txt():
    if request.method == "POST":
        print("text")
    return render_template("text-upload.html")

if __name__ == "__main__":
    app.run()