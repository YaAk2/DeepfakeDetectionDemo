from flask import Flask, request, jsonify, render_template, redirect
import pafy
import mimetypes
import requests
from io import BytesIO
import torch
import cv2
from PIL import Image
import os

from static.utils import img2out, vid2out


app = Flask(__name__)


@app.before_first_request
def load_model_to_app():
    app.predictor = torch.load('static/model/EfficientNetb0.model', map_location=torch.device("cpu"))
    
    
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get('URL') == 'URL':
            return render_template('url.html')
        if request.form.get('Files') == 'Files':
            return render_template('files.html')
        if request.form.get('tutorial') == 'tutorial':
            return render_template('tutorial.html')
    elif request.method == "GET":
        return render_template('index.html')
    
    
@app.route("/classify-file", methods=["GET", "POST"])
def classify_file():
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            if (file.mimetype).split('/')[0] == 'image':
                img = Image.open(file).convert('RGB')
                c = img2out(img, app.predictor)
            elif (file.mimetype).split('/')[0] == 'video':                
                file.save('tmp.mp4')
                video = cv2.VideoCapture('tmp.mp4')
                c = vid2out(video, app.predictor)  
                os.remove('tmp.mp4')
        return render_template("files.html", pred_from_file=c)
    elif request.method == "GET":
            return render_template('files.html')


@app.route("/classify-url", methods=["GET", "POST"])
def classify_url():
    if request.method == "POST":
        if request.form:
            url = request.form['url']
            if mimetypes.guess_type(url)[0]:
                if mimetypes.guess_type(url)[0].split('/')[0] == 'image':
                    response = requests.get(url)
                    img = Image.open(BytesIO(response.content))
                    c = img2out(img, app.predictor)
            elif not mimetypes.guess_type(url)[0]:
                video = pafy.new(url)
                best = video.getbest(preftype="mp4")
                video = cv2.VideoCapture()
                video.open(best.url)
                c = vid2out(video, app.predictor)            
        return render_template("url.html", pred_from_url=c)
    elif request.method == "GET":
        return render_template('url.html')

    
def main():
    """Run the app."""
    app.run(host='0.0.0.0')  # nosec

    
if __name__ == '__main__':
    main()
