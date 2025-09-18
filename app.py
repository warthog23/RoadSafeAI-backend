import os, uuid, datetime, base64
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from utils import save_file_from_request, save_base64_image, estimate_severity_from_detections
# Optional ultralytics import in infer.py

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
IMAGE_FOLDER = os.getenv("IMAGE_FOLDER", "./uploads")
MODEL_PATH = os.getenv("MODEL_PATH", "./yolov8_model/best.pt")
PORT = int(os.getenv("PORT", "5000"))

os.makedirs(IMAGE_FOLDER, exist_ok=True)

client = MongoClient(MONGO_URI)
db = client["roadsafe"]
reports = db["reports"]

app = Flask(__name__)
CORS(app)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status":"ok"})

@app.route("/upload", methods=["POST"])
def upload():
    """Accepts multipart/form-data 'file' OR JSON with image_base64.
       Required fields: lat, lon (float). Optional: run server-side inference.
    """
    try:
        if 'file' in request.files:
            img_path = save_file_from_request(request.files['file'], folder=IMAGE_FOLDER)
        else:
            data = request.get_json(force=True)
            img_b64 = data.get('image_base64')
            if not img_b64:
                return jsonify({"error":"No image provided"}), 400
            img_path = save_base64_image(img_b64, folder=IMAGE_FOLDER)

        # get coords
        lat = request.form.get('lat') or (request.json.get('lat') if request.is_json else None)
        lon = request.form.get('lon') or (request.json.get('lon') if request.is_json else None)
        if lat is None or lon is None:
            return jsonify({"error":"lat and lon required"}), 400
        lat, lon = float(lat), float(lon)

        # Optionally perform server-side inference if model exists
        detections = []
        severity = "unknown"
        try:
            from infer import run_inference_on_image
            detections = run_inference_on_image(img_path)
            severity = estimate_severity_from_detections(detections, img_path)
        except Exception as e:
            # model not available or inference failed - continue without inference
            print("Inference not run:", e)

        doc = {
            "image_path": img_path,
            "lat": lat,
            "lon": lon,
            "severity": severity,
            "detections": detections,
            "timestamp": datetime.datetime.utcnow(),
            "status": "reported"
        }
        res = reports.insert_one(doc)
        return jsonify({"success": True, "id": str(res.inserted_id), "severity": severity})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/potholes', methods=['GET'])
def list_potholes():
    docs = []
    for d in reports.find().sort('timestamp', -1).limit(1000):
        d['_id'] = str(d['_id'])
        # convert image path to URL (assuming same server serves images)
        d['image_url'] = request.url_root.rstrip('/') + '/images/' + os.path.basename(d['image_path'])
        docs.append(d)
    return jsonify({'reports': docs})

@app.route('/heatmap', methods=['GET'])
def heatmap():
    # returns list of [lat, lon, weight]
    points = []
    for d in reports.find():
        sev = d.get('severity','unknown')
        weight = 0.3
        if sev=='high': weight = 1.0
        elif sev=='medium': weight = 0.6
        elif sev=='low': weight = 0.3
        points.append([d.get('lat'), d.get('lon'), weight])
    return jsonify({'points': points})

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
