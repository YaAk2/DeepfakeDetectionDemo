from flask import Flask, request, render_template, redirect
import pafy
import mimetypes
import requests
from io import BytesIO
import torch
import cv2
import PIL
from PIL import Image
import os

from static.predict import img2out, vid2out


app = Flask(__name__)


@app.before_first_request
def load_model_to_app():
    app.predictor = torch.load('static/model/EfficientNetb0.model', map_location=torch.device("cpu"))
    

@app.route("/", methods=["GET", "POST"])
def home():
    return redirect('/home.html')

@app.route("/home.html", methods=["GET", "POST"])
def refresh_home():
    return render_template('home.html')


@app.route("/file.html", methods=["GET", "POST"])
def refresh_file():
    return render_template('file.html')

        
@app.route("/url.html", methods=["GET", "POST"])
def refresh_url():
    return render_template('url.html')

@app.route("/about.html", methods=["GET", "POST"])
def refresh_about():
    return render_template('about.html')

@app.route("/acknowledgements.html", methods=["GET", "POST"])
def refresh_acknowledge():
    return render_template('acknowledgements.html')


@app.route("/classify-file", methods=["Get", "POST"])
def classify_file():
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            if (file.mimetype).split('/')[0] == 'image':
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
        return render_template("file.html", pred_from_file=c)
    elif request.method == "GET":
        return render_template('file.html')


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
        return render_template("url.html", pred_from_url=c)
    elif request.method == "GET":
        return redirect('url.html')

def main():
    app.run(host='0.0.0.0') 

    
if __name__ == '__main__':
    main()
