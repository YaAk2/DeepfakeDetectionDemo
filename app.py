from flask import Flask, request, jsonify, render_template, redirect
import numpy as np
import torch
import torchvision
from torchvision import transforms
from PIL import Image
from facenet_pytorch import MTCNN
import cv2
import pafy
import mimetypes
import requests
from io import BytesIO
import os

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
    elif request.method == "GET":
        return render_template('index.html')
    
@app.route("/classify-file", methods=["GET", "POST"])
def classify_file():
    if request.method == "POST":
        detector = MTCNN(image_size=(256), post_process=False)
        
        if request.files:
            
            file = request.files["file"]
  
            if (file.mimetype).split('/')[0] == 'image':

                img = Image.open(file).convert('RGB')
                box, probs = detector.detect(img)
                if probs[0] and probs[0]>=0.25:
                    b = np.absolute(np.floor(box[0]).astype(dtype=np.int))
                    img = img.crop(b)
                    t = transforms.Compose([transforms.Resize((256, 256)), transforms.ToTensor()])
                    img = t(img).unsqueeze(0)
                    out = app.predictor(img)
                    out_max_idx = out.argmax()
                    if out_max_idx == 4: # Real
                        c = 'It is not a Deepfake!'
                    else:
                        c = 'It is a Deepfake!'
                else:
                    c = 'No face detected!'
            elif (file.mimetype).split('/')[0] == 'video':                
                file.save('tmp.mp4')
                video = cv2.VideoCapture('tmp.mp4')
                fps = int(video.get(cv2.CAP_PROP_FPS))
                frameCount = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
                fc = 0
                ret = True
                pred_idx = []
                cnt = 0
                
                while (fc < frameCount and ret):
                    ret, img = video.read()
                    if cnt==int(fps/fps) and ret:
                        box, probs = detector.detect(img)
                        if probs[0] and probs[0]>=0.25:
                            b = np.absolute(np.floor(box[0]).astype(dtype=np.int))
                            img = img[b[1]:b[3], b[0]:b[2]]
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            t = transforms.Compose([transforms.ToPILImage(), transforms.Resize((256, 256)), transforms.ToTensor()])
                            img = t(img).unsqueeze(0)
                            pred = app.predictor(img)
                            pred_idx.append(pred.argmax())  
                        cnt = 0
                    cnt += 1
                    fc += 1
                video.release()
                os.remove('tmp.mp4')

                if pred_idx:
                    if (np.asarray(pred_idx) ==4).sum()/len(pred_idx) > 0.5:
                        c = 'It is not a Deepfake!'
                    elif (np.asarray(pred_idx) ==4).sum()/len(pred_idx) <= 0.5:
                        c = 'It is a Deepfake!'
                else:
                    c = 'No face detected!'
                
        return render_template("files.html", pred_from_file=c)
    
    elif request.method == "GET":
            return render_template('files.html')


@app.route("/classify-url", methods=["GET", "POST"])
def classify_url():
    if request.method == "POST":
        detector = MTCNN(image_size=(256), post_process=False)
        if request.form:
            url = request.form['url']
            if mimetypes.guess_type(url)[0]:
                if mimetypes.guess_type(url)[0].split('/')[0] == 'image':
                    response = requests.get(url)
                    img = Image.open(BytesIO(response.content))
                    box, probs = detector.detect(img)
                    if probs[0] and probs[0]>=0.25:
                        b = np.absolute(np.floor(box[0]).astype(dtype=np.int))
                        img = img.crop(b)
                        t = transforms.Compose([transforms.Resize((256, 256)), transforms.ToTensor()])
                        img = t(img).unsqueeze(0)
                        pred = app.predictor(img)
                        pred_max_idx = pred.argmax()
                        if pred_max_idx == 4: # Real
                            c = 'It is not a Deepfake!'
                        else:
                            c = 'It is a Deepfake!' 
                    else:
                        c = 'No face detected!'
            elif not mimetypes.guess_type(url)[0]:
                video = pafy.new(url)
                best = video.getbest(preftype="mp4")
                video = cv2.VideoCapture()
                video.open(best.url)
                fps = int(video.get(cv2.CAP_PROP_FPS))
                frameCount = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
                fc = 0
                ret = True
                pred_idx = []
                cnt = 0

                while (fc < frameCount and ret):
                    ret, img = video.read()
                    if cnt==int(fps/fps) and ret:
                        box, probs = detector.detect(img)
                        if probs[0] and probs[0]>=0.25:
                            b = np.absolute(np.floor(box[0]).astype(dtype=np.int))
                            img = img[b[1]:b[3], b[0]:b[2]]
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            t = transforms.Compose([transforms.ToPILImage(), transforms.Resize((256, 256)), transforms.ToTensor()])
                            img = t(img).unsqueeze(0)
                            pred = app.predictor(img)
                            pred_idx.append(pred.argmax())  
                        cnt = 0
                    cnt += 1
                    fc += 1
                video.release()
                
                if pred_idx:
                    if (np.asarray(pred_idx) ==4).sum()/len(pred_idx) >= 0.5:
                        c = 'It is not a Deepfake!'
                    else:
                        c = 'It is a Deepfake!'
                else:
                     c = 'No face detected!'
        return render_template("url.html", pred_from_url=c)
    elif request.method == "GET":
        return render_template('url.html')

def main():
    """Run the app."""
    app.run(host='0.0.0.0')  # nosec

    
if __name__ == '__main__':
    main()
