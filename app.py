import os
import time
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify, session
from werkzeug.utils import secure_filename

from pdf_to_cards import pdf_OCR
from image_to_text import image_OCR
from text_to_cards import text_to_card

import threading
import markdown
import emoji
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'a_very_secret_key'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def session_clear():
    session.pop("cards", None)

@app.route('/', methods=['GET'])
def home():
    session_clear()
    open("input_note.txt","r").close()
    open("response.txt","r").close()
    return render_template("home.html")

@app.route('/pdf', methods=['GET', 'POST'])
def upload_pdf():
    session_clear()
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
    time.sleep(10)
    open("response.txt", "w").close()
    open("input_note.txt","r").close()


@app.route('/image', methods=['GET', 'POST'])
def upload_img():
    session_clear()
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
    session_clear()
    if request.method == "POST":
        res= request.form["textData"]
        with open('input_note.txt','w') as f:
            f.write(res)
            
        # clear the file
        open("response.txt", "w").close()
        
        threading.Thread(target=run_conversion).start()
        return redirect(url_for('download'))
    return render_template("text-upload.html")

@app.route('/converted', methods=["GET"])
def download():
    return render_template("convert.html")


@app.route('/check_status')
def check_status():
    try:
        data = None
        if os.stat("response.txt").st_size > 0:
            with open("response.txt", "r") as f:
                data = f.read()
                print(data)
            open("response.txt", "w").close()
            return jsonify({"ready":True,"data":data})
        return jsonify({"ready": False})
    except FileNotFoundError:
        return jsonify({"ready": False,"data":"Error occured."})

def run_conversion():
    text_to_card()
    reset()
    return "Flash card making started"

def reset():
    open("input_note.txt","r").close()
    print("Reset file")
    return

@app.route('/about')
def about():
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            readme_content = f.read()
            # Convert emoji shortcodes to actual emojis
            emojized_content = emoji.emojize(readme_content, language='en')
        
        # Convert Markdown with emojis to HTML
        html_content = markdown.markdown(emojized_content)
        
        return render_template('about.html', readme_html=html_content)
    except FileNotFoundError:
        return "README.md not found!", 404


if __name__ == "__main__":
    app.run()