from ultralytics import YOLO
import cv2

model=YOLO("models/yolo.pt")

def detect_buses(video_path):
    cap=cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret,frame=cap.read()
        if not ret:
            break

        results=model(frame)

        detections=[]
        for r in results:
            for box in r.boxes:
                cls=int(box.cls[0])
                conf=float(box.conf[0])

                if cls==5 and conf>0.5:
                    x1,y1,x2,y2=map(int,box.xyxy[0])
                    detections.append(([x1,y1,x2-x1,y2-y1],conf,"bus"))
                    cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

        cv2.imshow("Bus Detection",frame)
        if cv2.waitKey(1)==27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    detect_buses("data/video/bus_road.mp4")
