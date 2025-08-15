from ultralytics import YOLO
import cv2

# Paths
MODEL_PATH = r"E:\CHESS_OTB\chess\boardfinder.v3i.yolov11\runs\detect\train\weights\best.pt"
IMAGE_PATH = r"E:\CHESS_OTB\chess\new_img.jpg"

# Load image and model
image = cv2.imread(IMAGE_PATH)
model = YOLO(MODEL_PATH)  # load your custom model

# Run inference
results = model(IMAGE_PATH)  # can pass the path directly
final_list = []
# Process results
for result in results:
    square_detections = []
    for box in result.boxes: 
        conf = float(box.conf[0]) 
        cls_id = int(box.cls[0]) 
        class_name = model.names[cls_id]  
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        
        # Correct center calculation
        center_x = int((x1 + x2) // 2)
        center_y = int(y2 - (y2 - y1) // 4 )
        center = (center_x, center_y)
        
        square_detections.append((center, class_name, conf))
        
        # Draw center point and label
        cv2.circle(image, center, 5, (0, 0, 255), -1)
        cv2.putText(image, f"{class_name} {conf:.2f}", 
                    (center_x - 20, center_y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        print(f"Detected {class_name} (conf: {conf:.2f}) at {center}")
        final_list.append((center , class_name))

# Display and save results
cv2.imshow("Detected Chess Pieces", image) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 
cv2.imwrite("chess_pieces_detected.jpg", image)
print(center)
# Optional: Save detections to a text file
with open("detections.txt", "w") as f:
    for center, class_name, conf in square_detections:
        f.write(f"{class_name} {center[0]} {center[1]} {conf:.4f}\n")

print(final_list)