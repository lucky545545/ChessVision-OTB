from ultralytics import YOLO 
import cv2 
import os 
 
# Load your trained model  
model = YOLO(r"C:\Users\TUF\OneDrive\Desktop\chess\boardfinder.v3i.yolov11\runs\detect\train\weights\best.pt")  
 
# Run inference  
results = model([r"C:\Users\TUF\OneDrive\Desktop\chess\new_img.jpg"]) 
 
# Load the same image with OpenCV 
image_path = r"C:\Users\TUF\OneDrive\Desktop\chess\new_img.jpg" 
image = cv2.imread(image_path) 
 
# Threshold 

TARGET_CLASS = "square"  # Change this to your actual class name 
 
# List to store all valid square detections
square_detections = []

# Collect all valid square detections
for result in results: 
    boxes = result.boxes 
    for box in boxes: 
        conf = float(box.conf[0]) 
        cls_id = int(box.cls[0]) 
        class_name = model.names[cls_id] 

        if  class_name == TARGET_CLASS: 
            x1, y1, x2, y2 = box.xyxy[0].tolist() 
            center = (int((x1 + x2) // 2), int((y1 + y2) // 2)) 
            square_detections.append((conf, center, class_name))

# Sort by confidence descending and select top 64
square_detections.sort(reverse=True, key=lambda x: x[0])
top_squares = square_detections[:64]
print(top_squares)
# Draw and count top squares
count = 0
for conf, center, class_name in top_squares:
    count += 1
    x, y = center
    cv2.circle(image, center, 3, (0, 0, 255), -1)  # red dot
    # Draw coordinates as text near the center point
    cv2.putText(image, f"({x},{y})", (x + 5, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    print(f"Detected {class_name} with confidence {conf:.2f} at center {center}")

# Optional: Show the count on image
cv2.putText(image, f"Top Squares Detected: {count}", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Show final result with only top square centers and coordinates
cv2.imshow("Top 64 Squares Detected", image) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 

# Optional: save output image 
cv2.imwrite("squares_detected.jpg", image) 

print(f"Total top squares drawn: {count}")
