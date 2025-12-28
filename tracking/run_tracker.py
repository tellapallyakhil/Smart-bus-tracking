import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# Load YOLOv8 model (pretrained)
model = YOLO("yolov8n.pt")

# Initialize DeepSORT
tracker = DeepSort(
    max_age=30,
    n_init=3,
    max_cosine_distance=0.2
)

# Path to video file
VIDEO_PATH = "data/video/bus_road.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO inference
    results = model(frame, conf=0.5, iou=0.5)

    detections = []

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])

            # COCO class 5 = bus
            if cls_id == 5:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                w, h = x2 - x1, y2 - y1
                detections.append(([x1, y1, w, h], conf, "bus"))

    # Update tracker
    tracks = tracker.update_tracks(detections, frame=frame)

    # Draw results
    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l, t, r, b = map(int, track.to_ltrb())

        cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"Bus ID: {track_id}",
            (l, t - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    cv2.imshow("Smart Bus Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
