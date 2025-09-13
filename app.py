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

@app.route('/converted', methods=["GET"])
def download():
    return render_template("convert.html")

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
                return "File saved successfully"
        return "No pdf file provide"
    return render_template("pdf-upload.html")

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
                return "File saved successfully"
        return "No image provide"
    return render_template("image-upload.html")

@app.route('/text', methods=['GET', 'POST'])
def upload_txt():
    if request.method == "POST":
        res= request.form["textData"]
        return res
    return render_template("text-upload.html")






if __name__ == "__main__":
    app.run()