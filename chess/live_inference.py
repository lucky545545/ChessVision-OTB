import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLO model
model = YOLO(r"E:\CHESS_OTB\chess\boardfinder.v3i.yolov11\runs\detect\train\weights\best.pt")  # Replace with your model path
TARGET_CLASS = "square"  # Class name for squares
EXPECTED_SQUARES = 64  # 8x8 chessboard

def order_squares_to_chessboard(sq_list, rows=8, cols=8):
    """Sort detected squares into chessboard order (A1-H8)."""
    if len(sq_list) != rows * cols:
        print(f"Warning: Expected {rows * cols} squares, got {len(sq_list)}")

    centers = np.array(sq_list)
    y_sorted = centers[np.argsort(centers[:, 1])]  # Sort by Y (rows)
    
    board = []
    for i in range(rows):
        row = y_sorted[i*cols : (i+1)*cols]
        row = row[np.argsort(row[:, 0])]  # Sort row by X (left to right)
        board.append(row)
    
    return board[::-1]  # Reverse rows (chessboard starts at bottom)

def draw_chessboard_labels(frame, board):
    """Draw chess notation (A1-H8) on the frame."""
    ranks = [str(i+1) for i in range(8)]  # 1-8 (bottom to top)
    files = ['H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']  # Left to right

    for i, row in enumerate(board):
        for j, (x, y) in enumerate(row):
            square_name = f"{files[j]}{ranks[i]}"
            cv2.putText(frame, square_name, (int(x)-20, int(y)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Initialize webcam
cap = cv2.VideoCapture(0)  # Use 0 for default camera

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO inference
    results = model(frame, verbose=False)  # Disable logging for speed

    # Process detections
    square_centers = []
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            if model.names[cls_id] == TARGET_CLASS and conf > 0.5:  # Confidence threshold
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                center = (int((x1 + x2) / 2), int((y1 + y2) / 2))
                square_centers.append(center)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)  # Mark center

    # If we found all squares, label them
    if len(square_centers) == EXPECTED_SQUARES:
        chessboard = order_squares_to_chessboard(square_centers)
        draw_chessboard_labels(frame, chessboard)
    else:
        cv2.putText(frame, f"Squares: {len(square_centers)}/{EXPECTED_SQUARES}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display
    cv2.imshow("Chessboard Detection", frame)
    if cv2.waitKey(1) == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()