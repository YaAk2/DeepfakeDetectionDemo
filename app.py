from flask import Flask, request, render_template, redirect, jsonify, url_for
import pafy
import mimetypes
import requests
from io import BytesIO
import torch
import cv2
import PIL
from PIL import Image
import os
from werkzeug.utils import secure_filename

from static.predict import img2out, vid2out


#
import base64
#

app = Flask(__name__)


@app.before_first_request
def load_model_to_app():
    app.predictor = torch.load('static/model/EfficientNetb0.model', map_location=torch.device("cpu"))
    

@app.route("/", methods=["GET", "POST"])
def welcome():
    return redirect('/welcome.html')

@app.route("/welcome.html", methods=["GET", "POST"])
def refresh_welcome():
     return render_template('welcome.html')

# @app.route("/file.html", methods=["GET", "POST"])
# def refresh_file():
#     return render_template('file.html')

        
@app.route("/deepfakedetection.html", methods=["GET", "POST"])
def refresh_dfd():
    return render_template('deepfakedetection.html')

@app.route("/technical.html", methods=["GET", "POST"])
def refresh_technical():
    return render_template('technical.html')

@app.route("/acknowledgements.html", methods=["GET", "POST"])
def refresh_acknowledge():
    return render_template('acknowledgements.html')

@app.route("/classify-file", methods=["Get", "POST"])
def classify_file():
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            if (file.mimetype).split('/')[0] == 'image':
                file = request.files['file']
                try:
                    img = Image.open(file).convert('RGB')
                    c = img2out(img, app.predictor)
                except PIL.UnidentifiedImageError:
                    c = 'Please check if the uploaded file a valid image/video format'        
            elif (file.mimetype).split('/')[0] == 'video':                
                try:
                    file.save('tmp.mp4')
                    video = cv2.VideoCapture('tmp.mp4')
                    c = vid2out(video, app.predictor)  
                    os.remove('tmp.mp4')
                except:
                    c = 'Please check if the uploaded file a valid image/video format'
    elif request.method == "GET":
        return redirect('deepfakedetection.html')
    try:
        return render_template("deepfakedetection.html", pred_from_file=c)
    except UnboundLocalError:
        c = 'Please check if the uploaded file a valid image/video format'
        return render_template("deepfakedetection.html", pred_from_file=c)


@app.route("/classify-url", methods=["GET", "POST"])
def classify_url():
    if request.method == "POST":
        if request.form:
            url = request.form['url']
            if mimetypes.guess_type(url)[0]:
                if mimetypes.guess_type(url)[0].split('/')[0] == 'image':
                    response = requests.get(url)
                    try:
                        img = Image.open(BytesIO(response.content))
                        c = img2out(img, app.predictor)
                    except PIL.UnidentifiedImageError:
                        c = 'Please check if the URL is valid'
            elif not mimetypes.guess_type(url)[0]:
                try: 
                    video = pafy.new(url)
                    best = video.getbest(preftype="mp4")
                    video = cv2.VideoCapture()
                    video.open(best.url)
                    c = vid2out(video, app.predictor)
                except ValueError:
                    c = 'Please check if the URL is valid'
    elif request.method == "GET":
        return redirect('deepfakedetection.html')
    return render_template("deepfakedetection.html", pred_from_url=c)

def main():
    app.run(host='0.0.0.0') 

    
if __name__ == '__main__':
    main()
