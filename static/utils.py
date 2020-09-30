import numpy as np
import torchvision
from torchvision import transforms
from facenet_pytorch import MTCNN
import cv2


detector = MTCNN(image_size=(256), post_process=False)


def img2out(img, model):
    box, probs = detector.detect(img)
    if probs[0] and probs[0]>=0.25:
        b = np.absolute(np.floor(box[0]).astype(dtype=np.int))
        img = img.crop(b)
        t = transforms.Compose([transforms.Resize((256, 256)), transforms.ToTensor()])
        img = t(img).unsqueeze(0)
        pred = model(img)
        pred_max_idx = pred.argmax()
        if pred_max_idx == 4: # Real
            c = 'It is not a Deepfake!'
        else:
            c = 'It is a Deepfake!'
    else:
        c = 'No face detected!'
    return c


def vid2out(video, model):
    fps = int(video.get(cv2.CAP_PROP_FPS))
    frameCount = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fc = 0
    ret = True
    pred_max_ids = []
    cnt = 0

    while (fc < frameCount and ret):
        ret, img = video.read()
        if cnt==int(fps/2) and ret:
            box, probs = detector.detect(img)
            if probs[0] and probs[0]>=0.25:
                b = np.absolute(np.floor(box[0]).astype(dtype=np.int))
                img = img[b[1]:b[3], b[0]:b[2]]
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                t = transforms.Compose([transforms.ToPILImage(), transforms.Resize((256, 256)), transforms.ToTensor()])
                img = t(img).unsqueeze(0)
                pred = model(img)
                pred_max_ids.append(pred.argmax())  
            cnt = 0
        cnt += 1
        fc += 1
    video.release()

    if pred_max_ids:
        if (np.asarray(pred_max_ids) ==4).sum()/len(pred_max_ids) > 0.5:
            c = 'It is not a Deepfake!'
        elif (np.asarray(pred_max_ids) ==4).sum()/len(pred_max_ids) <= 0.5:
            c = 'It is a Deepfake!'
    else:
        c = 'No face detected!'  
    return c