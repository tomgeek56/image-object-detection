import numpy as np
import cv2
import os
from django.conf import settings
import base64
import urllib
from detection.models import DetectionObject

def detectObjects(image_base64):
    #przeniesc do settingsow
    weights_path = os.path.join(settings.STATIC_ROOT, 'ai\\yolov3.weights')
    cfg_path = os.path.join(settings.STATIC_ROOT, 'ai\\yolov3.cfg')
    coco_path = os.path.join(settings.STATIC_ROOT, 'ai\\coco.names')
    text_image_path = os.path.join(settings.STATIC_ROOT, 'ai\\room_ser.jpg')

    net = cv2.dnn.readNet(weights_path, cfg_path)

    with open(coco_path, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1]
                     for i in net.getUnconnectedOutLayers()]

    imgdata = base64.b64decode(str(image_base64))
    image_uint8 = np.fromstring(imgdata, dtype="uint8")

    ##### NEW CODE ####
    img = cv2.imdecode(image_uint8, cv2.IMREAD_COLOR)
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(
        img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    
    detections = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                label = str(classes[class_id])
                detection = DetectionObject()
                detection.set((x, y, w, h, label, class_id))
                detections.append(detection)
    
    return detections
