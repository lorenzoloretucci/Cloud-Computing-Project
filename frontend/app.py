from flask import Flask,render_template, request, redirect, send_file, url_for, send_from_directory,Response
from werkzeug.utils import secure_filename
import boto3
import requests
import os
app = Flask(__name__)

image_counter = 0

@app.route("/")
def storage(msg_1=" ",msg_2=" "):
    render_template('storage.html',msg_1=msg_1,msg_2=msg_2)
    return render_template('storage.html',msg_1=msg_1,msg_2=msg_2)


@app.route("/feed_back", methods = ["POST"])
def save_feed():
    global image_counter
    if request.method == 'POST':
        is_correct = str(request.form.get("yes_or_no_group"))
        file_name =request.form.get("file_name")
        if is_correct == "yes" :
            print(is_correct)
            return storage(msg_1="Thanks for your precious feed back!",msg_2="Retry it!")
        elif is_correct == "no" :
            print(is_correct)
            return render_template("storage2.html",datas="comp_select",
                                   data=[{'name': '-'},{'name': 'sea'}, {'name': 'mountain'},
                                         {'name': 'forest'}, {'name': 'street'},{'name': 'buildings'},
                                         {'name': 'glacier'}],file_name=file_name)
        else:
            with open("correct_labels.csv","a") as f:
                f.write("{},{}\n".format(file_name,request.form.get("comp_select")))

            print(request.form.get("comp_select"))
            image_counter += 1
            if image_counter == 100 :
                s3 = boto3.resource("s3")
                s3.meta.client.upload_file("correct_labels.csv","clc-project-mlmodels","correct_labels.csv")
                image_counter =0
                os.remove("correct_labels.csv")

            return storage(msg_1="Thanks for your precious feed back!",msg_2="Retry it!")

@app.route("/up", methods=["POST"])
def upload_file():
    if request.method == 'POST':
        image_file = request.files['image_file']
        content_type = request.mimetype
        if image_file:
            file_name = secure_filename(image_file.filename)
            file_upload_name = "uploaded_image/"+file_name
            client = boto3.client('s3')
            client.put_object(Body=image_file,
                              Bucket="userimages",
                              Key=file_upload_name,
                              ContentType=content_type)

            output = requests.get("https://rffu2kkte2.execute-api.us-east-1.amazonaws.com/image_classifier",
                              params={'image_name': file_name})
            output = output.json()
            return render_template('storage2.html', label=output["url"], file_name=file_name, datas="radio_type")
        else:
            return storage(msg_1="You must upload a picture")
@app.route("/health_check",methods=["GET"])
def health_check():
    return Response(status=200)




if __name__ == '__main__':

    app.run("0.0.0.0",port=5000,debug=True)
