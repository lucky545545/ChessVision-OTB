import cv2

# Load the image
image = cv2.imread("test.jpg")  # Replace with your actual image path

# YOLO bounding box in [x1, y1, x2, y2] format
bbox = [290, 201, 397, 255]

# Unpack the coordinates
x1, y1, x2, y2 = bbox
center = ((x1 + x2) // 2, (y1 + y2) // 2)
# Draw rectangle on image
cv2.circle(image,center, 2, (0,0,255), -1)
#cv2.rectangle(image, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)

# Optionally add label
label = "Detected Object"
cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
            fontScale=0.6, color=(0, 255, 0), thickness=2)

# Show image
cv2.imshow("Image with Bounding Box", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Optional: Save the image
cv2.imwrite("boxed_image.jpg", image)
