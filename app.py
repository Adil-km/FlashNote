import os
import time
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename

from pdf_to_cards import pdf_OCR
from image_to_text import image_OCR
from text_to_cards import text_to_card

import threading

UPLOAD_FOLDER = 'temp_uploads'
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
        if "pdfFile" in request.files:
            file = request.files["pdfFile"]
            if file.filename != '':
                filename = secure_filename(file.filename)
                upload_dir = 'static/uploads'
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, filename)
                file.save(file_path)
 
                threading.Thread(target=process_file, args=("pdf",file_path)).start()
                return redirect(url_for('download'))
            
        return "No valid PDF file provided"
    return render_template("pdf-upload.html")

def process_file(file_type,file_path):
    if file_type=="pdf":
        pdf_OCR(file_path)
    elif file_type == "img":
        image_OCR(file_path)
    else:
        return "An error occurred: file type not valid"
    text_to_card() 
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print("File not found:", file_path)

@app.route('/image', methods=['GET', 'POST'])
def upload_img():
    if request.method == "POST":
        if "imageFile" in request.files:
            file = request.files["imageFile"]
            if file.filename != '':
                filename = secure_filename(file.filename)
                upload_dir = 'static/uploads'
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, filename)
                file.save(file_path)

                threading.Thread(target=process_file, args=("img",file_path)).start()
                return redirect(url_for('download'))
            
        return "No image provided"
    return render_template("image-upload.html")

@app.route('/text', methods=['GET', 'POST'])
def upload_txt():
    if request.method == "POST":
        res= request.form["textData"]
        with open('input_note.txt','w') as f:
            f.write(res)
            
        # clear the file
        open("response.txt", "w").close()
        
        time.sleep(1)
        threading.Thread(target=run_conversion).start()
        return redirect(url_for('download'))
    return render_template("text-upload.html")

@app.route('/converted', methods=["GET"])
def download():
    return render_template("convert.html")


@app.route('/check_status')
def check_status():
    try:
        return jsonify({"ready": os.stat("response.txt").st_size > 0})
    except FileNotFoundError:
        return jsonify({"ready": False})

def run_conversion():
    text_to_card()
    return "Flash card making started"

if __name__ == "__main__":
    app.run()