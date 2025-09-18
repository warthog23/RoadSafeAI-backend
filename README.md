# RoadSafeAI - Backend (Flask + YOLOv8 + MongoDB)

## What's included
- `app.py` : Main Flask app (upload, list potholes, heatmap endpoints)
- `infer.py` : Small wrapper to run YOLOv8 inference if you place a model
- `utils.py` : Helper functions (save image, severity heuristic)
- `requirements.txt` : Python dependencies
- `.env.example` : Example environment variables
- `Dockerfile` and `Procfile` : Deployment helpers
- `uploads/` : Folder where uploaded images are stored (created empty)
- `yolov8_model/` : Place your trained `best.pt` or exported model here

## Quick start (local)
1. Create virtual env: `python -m venv venv && source venv/bin/activate`
2. Install: `pip install -r requirements.txt`
3. Copy `.env.example` -> `.env` and edit `MONGO_URI`, optionally `MODEL_PATH`
4. Run: `python app.py`
5. Use a tool like Postman or the included example curl to upload images.

## Upload example (curl)
```bash
curl -X POST http://127.0.0.1:5000/upload \
  -F "file=@path/to/road.jpg" \
  -F "lat=26.9124" -F "lon=75.7873"
```

## Notes
- This repo does not include a trained YOLOv8 model due to size. Place your `best.pt` or ONNX file in `yolov8_model/` and set `MODEL_PATH` in `.env`.
- For production, configure S3/Cloudinary for images and secure your DB credentials.
