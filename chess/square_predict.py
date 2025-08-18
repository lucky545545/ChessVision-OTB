from ultralytics import YOLO 
import cv2 
import os 
import numpy as np

# Configuration
MODEL_PATH = r"E:\CHESS_OTB\chess\boardfinder.v3i.yolov11\runs\detect\train\weights\best.pt"
IMAGE_PATH = r"E:\CHESS_OTB\chess\WhatsApp Image 2025-08-09 at 17.57.17_0eab8d1e.jpg"
TARGET_CLASS = "square"
EXPECTED_SQUARES = 64

def main():
    clock_side = "right_w"  # Change this to "left_w" if needed
    # Load model and image
    model = YOLO(MODEL_PATH) 
    image = cv2.imread(IMAGE_PATH)
    
    if image is None:
        print(f"Error: Could not load image at {IMAGE_PATH}")
        return

    # Run inference 
    results = model([IMAGE_PATH]) 
    
    # Process results
    square_detections = []
    for result in results: 
        for box in result.boxes: 
            conf = float(box.conf[0]) 
            cls_id = int(box.cls[0]) 
            class_name = model.names[cls_id] 

            if class_name == TARGET_CLASS: 
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                center = (int((x1 + x2) // 2), int((y1 + y2) // 2))
                square_detections.append((conf, center, class_name))

    # Sort and select top detections
    square_detections.sort(reverse=True, key=lambda x: x[0])
    top_squares = square_detections[:EXPECTED_SQUARES]

    # Visualize results
    count = 0
    sq_list = []
    for conf, center, class_name in top_squares:
        sq_list.append(center)
        count += 1
        cv2.circle(image, center, 3, (0, 0, 255), -1)
        #print(f"Detected {class_name} {count:02d}: confidence {conf:.2f} at {center}")

    # Add count to image
    cv2.putText(image, f"Squares Detected: {count}/{EXPECTED_SQUARES}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show and save results
    cv2.imshow("Detected Squares", image) 
    cv2.waitKey(0) 
    cv2.destroyAllWindows() 
    cv2.imwrite("squares_detected.jpg", image) 

    # Print all centers and optionally sort them
    print("\nAll centers:")
    for i, center in enumerate(sq_list, 1):
        print(f"{i:02d}. {center}")

    # Optional: Sort by height
    print("\nSorted by height (Y coordinate):")
    sorted_by_y = sorted(sq_list, key=lambda coord: coord[1])
    for i, center in enumerate(sorted_by_y, 1):
        print(f"{i:02d}. {center}")
    board = order_squares_to_chessboard(sq_list)
    print_chessboard_labels(board ,clock_side)



def order_squares_to_chessboard(sq_list, rows=8, cols=8):
    """
    Takes a list of (x, y) centers and sorts them into chessboard order (A1-H8).
    Returns a 2D list where board[0][0] = A1, board[0][1] = B1, ..., board[7][7] = H8.
    """
    if len(sq_list) != rows * cols:
        print(f"Warning: Expected {rows * cols} squares, but got {len(sq_list)}")
    # Convert to numpy array for easier manipulation
    centers = np.array(sq_list)
    # Step 1: Sort by Y-coordinate (rows)
    y_sorted = centers[np.argsort(centers[:, 1])]
    # Step 2: Split into rows and sort each row by X-coordinate (left to right)
    
    board = []
    for i in range(rows):
        row_start = i * cols
        row_end = (i + 1) * cols
        row = y_sorted[row_start:row_end]
        row = row[np.argsort(row[:, 0])]  # Sort row by X-coordinate
        board.append(row)
    # Step 3: Reverse row order (chessboard starts at bottom-left)
    
    return board
def print_chessboard_labels(board , clock_side):
    """
    Prints the board with chess notation (A1-H8).
    """
    
    ranks = ['1', '2' , '3' , '4' , '5' , '6' , '7' , '8']  
    files = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    if clock_side == "right_w":
        ranks = ranks[::-1]  
        files = files[::-1]  
        for i, row in enumerate(board):
            for j, (x, y) in enumerate(row):
                square_name = f"{files[i]}{ranks[j]}"
                print(f"{square_name}: Center at ({x}, {y})")
    elif clock_side == "left_w":
        for i, row in enumerate(board):
            for j, (x, y) in enumerate(row):
                square_name = f"{files[i]}{ranks[j]}"
                print(f"{square_name}: Center at ({x}, {y})")

if __name__ == "__main__":
    main()
