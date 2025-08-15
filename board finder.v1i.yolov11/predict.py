from ultralytics import YOLO

# Load your custom-trained model
model = YOLO("/home/lakshayg/CHESS/board finder.v1i.yolov11/runs/detect/train3/weights/best.pt")

# Run inference
results = model(["/home/lakshayg/CHESS/board finder.v1i.yolov11/board_test.jpg"])

# Confidence threshold
CONF_THRESHOLD = 0.50
count = 0
# Process each result
for result in results:
    boxes = result.boxes
    for box in boxes:
        conf = float(box.conf[0])  # confidence score
        if conf >= CONF_THRESHOLD:
            count += 1
            cls_id = int(box.cls[0])  # class ID
            x1, y1, x2, y2 = box.xyxy[0].tolist()  # bounding box coordinates
            print(f"Detected {model.names[cls_id]} with confidence {conf:.2f} at [{x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f}]")

    result.show()  # optional: display image with all boxes
    result.save(filename="result.jpg")  # optional: save image
print(count)