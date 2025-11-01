from ultralytics import YOLO
ai = YOLO("runs/detect/train6/weights/best.pt")
ai(source="test.mp4",show = True,save = True)