import os

from os.path import join, dirname, realpath

from flask import Flask, render_template, request, redirect, send_file, url_for

from s3_demo import list_files, download_file, upload_file, image_predict

import tensorflow as tf

from werkzeug.utils import secure_filename


#upload image
#UPLOAD_FOLDER = "uploads"
UPLOAD_FOLDER= join(dirname(realpath(__file__)), 'uploads/')
app = Flask(__name__)
#BUCKET = "insert_bucket_name_here"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


##Load Model 
MODEL_PATH = "flask-drive\models\model_inc.h5"
model = tf.keras.models.load_model(MODEL_PATH)


#render main image
@app.route("/")
def storage():
    contents = list_files("flaskdrive")
    return render_template('storage.html', contents=contents)

@app.route("/", methods = ["POST", "GET"])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']

        if f :
            filename = secure_filename(f.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print('file_path')
            f.save(file_path)
            output = image_predict(file_path, model)
    
    return render_template('storage.html', label = output )

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

''''
@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(f.filename)
        upload_file(f"{f.filename}", BUCKET)

        return redirect("/")


@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)
'''

if __name__ == '__main__':
    app.run(debug=True)
