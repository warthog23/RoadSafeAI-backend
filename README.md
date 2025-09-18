#  RoadSafeAI – Smart Pothole Detection & Reporting System (Backend)

RoadSafeAI is an AI-powered system that detects road potholes/cracks using **Computer Vision (YOLOv8)**, geo-tags them with **GPS coordinates**, and reports them via a **Flask backend + MongoDB database**.  
This repository contains the backend service for RoadSafeAI.

---

##  What's Included
- `app.py` → Main Flask app (upload, list potholes, heatmap endpoints)
- `infer.py` → Wrapper to run YOLOv8 inference on road images
- `utils.py` → Helper functions (save image, severity scoring, etc.)
- `requirements.txt` → Python dependencies
- `.env.example` → Example environment variables
- `Dockerfile` + `Procfile` → Deployment helpers (Heroku/Railway)
- `uploads/` → Stores uploaded road images (empty by default)
- `yolov8_model/` → Place your trained `best.pt` or exported model here

---

##  Tech Stack
- **Backend**: Flask (Python)
- **Computer Vision**: YOLOv8 (Ultralytics)
- **Database**: MongoDB / MongoDB Atlas
- **Deployment**: Docker, Railway / Heroku
- **API Testing**: Postman / curl

---

##  Quick Start (Local)

```bash
# 1️ Create virtual environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

# 2️ Install dependencies
pip install -r requirements.txt

# 3️ Configure environment
cp .env.example .env
# Update .env with:
# MONGO_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/db
# MODEL_PATH=./yolov8_model/best.pt

# 4️ Run server
python app.py
```

Server will run at: **http://127.0.0.1:5000**

---

##  API Endpoints

### 1. Upload pothole image
```bash
POST /upload
```
**Params:**  
- `file` → Image of road (required)  
- `lat` → Latitude (required)  
- `lon` → Longitude (required)  

**Example:**
```bash
curl -X POST http://127.0.0.1:5000/upload   -F "file=@path/to/road.jpg"   -F "lat=26.9124" -F "lon=75.7873"
```

---

### 2. Get all potholes
```bash
GET /potholes
```
Returns recent pothole detections with metadata (location, severity, timestamp).

---

### 3. Heatmap data
```bash
GET /heatmap
```
Returns geo-coordinates of potholes for visualization on Google Maps / Leaflet.

---

##  Notes
-  This repo **does not include a trained YOLOv8 model** due to size.  
  Place your `best.pt` or `model.onnx` inside `yolov8_model/` and set `MODEL_PATH` in `.env`.
- For production:
  - Use **S3/Cloudinary** for image storage
  - Secure MongoDB credentials
  - Use Docker + Railway/Heroku for deployment

---

##  Roadmap
- [ ] Multi-class road damage detection (potholes, cracks, patches)  
- [ ] User authentication for municipal dashboards  
- [ ] Citizen mobile app integration (React Native frontend)  
- [ ] Automated repair status updates  

---

##  Contribution
Pull requests are welcome!  
For major changes, please open an issue first to discuss what you would like to change.  

---

##  License
This project is licensed under the **MIT License** – free to use and modify.

---

##  Author
Developed as part of **Smart City AI Project** by Gajendra Singh.
