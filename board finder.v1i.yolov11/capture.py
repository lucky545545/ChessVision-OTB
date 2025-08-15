import cv2

# Initialize webcam (0 = default camera)
cap = cv2.VideoCapture(0)

# Check if the camera is opened
if not cap.isOpened():
    print("Cannot open camera")
    exit()

captured_image = None

print("Press SPACE or ENTER to capture an image. Press ESC to exit.")

while True:
    ret, frame = cap.read()  # Read frame-by-frame
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Webcam - Press SPACE to Capture", frame)

    key = cv2.waitKey(1)

    if key == 27:  # ESC key to exit
        break
    elif key in [13, 32]:  # Enter or Space to capture
        captured_image = frame.copy()
        print("Image captured!")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

# If image was captured, you can use it further
if captured_image is not None:
    # Optional: Save to disk
    cv2.imwrite("captured.jpg", captured_image)
    print("Saved as 'captured.jpg'")
