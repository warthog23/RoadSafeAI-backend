# infer.py - wrapper to run YOLOv8 inference using ultralytics
# Place your trained best.pt in yolov8_model/ and set MODEL_PATH accordingly.
from ultralytics import YOLO
import os
import cv2

MODEL_PATH = os.getenv('MODEL_PATH', './yolov8_model/best.pt')
model = None
try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print('Could not load model:', e)

def run_inference_on_image(image_path, conf_thresh=0.3):
    """Runs model on image and returns list of detections:
       [ {'bbox':[x1,y1,x2,y2], 'conf':0.9, 'class':0}, ... ]"""
    if model is None:
        raise RuntimeError('Model not loaded')
    results = model(image_path)
    out = []
    for r in results:
        for box in r.boxes:
            x1,y1,x2,y2 = [float(x) for x in box.xyxy[0].tolist()]
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            if conf < conf_thresh: continue
            out.append({'bbox':[x1,y1,x2,y2], 'conf':conf, 'class':cls})
    return out
