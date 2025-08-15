from ultralytics import YOLO
import cv2
import numpy as np
def detect_squares(model_path, image_path, target_class="square", expected_squares=64):
    """Detects squares in a chessboard image and returns their centers."""
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    
    model = YOLO(model_path)
    results = model(image)
    
    square_detections = []
    for result in results:
        for box in result.boxes: 
            conf = float(box.conf[0]) 
            cls_id = int(box.cls[0]) 
            class_name = model.names[cls_id] 

            if class_name == target_class: 
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                center = (int((x1 + x2) // 2), int((y1 + y2) // 2))
                square_detections.append((conf, center, class_name))

    # Sort and select top detections
    square_detections.sort(reverse=True, key=lambda x: x[0])
    top_squares = square_detections[:expected_squares]
    return top_squares


def order_squares_to_chessboard(sq_list = detect_squares, rows=8, cols=8):
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
def print_chessboard_labels( board = order_squares_to_chessboard , clock_side = "right_w", final_sq_list= [] ):
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
                final_sq_list.append((square_name,(x, y)))
    
    elif clock_side == "left_w":
        for i, row in enumerate(board):
            for j, (x, y) in enumerate(row):
                square_name = f"{files[i]}{ranks[j]}"
                final_sq_list.append((square_name,(int(x),int(y))))

    return final_sq_list


def get_squares(model_path, image_path, target_class="square",
                      expected_squares=64, clock_side="right_w"):
    """
    End-to-end helper:
    1. detect squares
    2. order them into a chessboard grid
    3. print chessboard-style labels
    4. return the same list produced by print_chessboard_labels
    """
    if isinstance(image_path, str):
        img = cv2.imread(image_path)
    else:
        img = image_path.copy()
    # 1. Detect
    detections = detect_squares(model_path, image_path, target_class, expected_squares)
    # detections = [(conf, (x, y), class_name), ...]

    # 2. Order
    # strip the confidence and the class name, keep only the (x,y) centers
    centers = np.array([center for _, center, _ in detections])
    board = order_squares_to_chessboard(centers)

    # 3. Print and capture the final list
    final_list = print_chessboard_labels(board, clock_side=clock_side)
    return final_list






def get_pieces(model_path, image_path):
    """Detects chess pieces and returns their centers and class names."""
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    
    model = YOLO(model_path)
    results = model(image)
    
    square_detections = []
    for result in results:
        for box in result.boxes: 
            conf = float(box.conf[0]) 
            cls_id = int(box.cls[0]) 
            class_name = model.names[cls_id]  
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            center_x = int((x1 + x2) // 2)
            center_y = int(y2 - (y2 - y1) // 4)
            square_detections.append(((center_x, center_y), class_name))
    
    return square_detections
