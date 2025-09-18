import os, uuid, base64, cv2

def save_file_from_request(file_storage, folder='./uploads'):
    fname = f"{uuid.uuid4().hex}.jpg"
    path = os.path.join(folder, fname)
    file_storage.save(path)
    return path

def save_base64_image(b64string, folder='./uploads'):
    header, data = (b64string.split(',',1) + [None])[:2]
    if data is None:
        data = header  # no header present
    fname = f"{uuid.uuid4().hex}.jpg"
    path = os.path.join(folder, fname)
    with open(path, 'wb') as f:
        f.write(base64.b64decode(data))
    return path

def bbox_area(bbox):
    x1,y1,x2,y2 = bbox
    return max(0,(x2-x1)) * max(0,(y2-y1))

def estimate_severity_from_detections(detections, img_path):
    # very simple heuristic using largest bbox area ratio
    if not detections:
        return 'unknown'
    img = cv2.imread(img_path)
    if img is None:
        return 'unknown'
    img_area = img.shape[0]*img.shape[1]
    largest = 0
    for det in detections:
        bbox = det.get('bbox')
        if not bbox: continue
        area = bbox_area(bbox)
        largest = max(largest, area)
    ratio = largest / img_area
    if ratio > 0.02:
        return 'high'
    elif ratio > 0.005:
        return 'medium'
    else:
        return 'low'
