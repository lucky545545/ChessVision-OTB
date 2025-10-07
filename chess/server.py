import os, io, base64, threading
from flask import Flask, request, send_file, jsonify
import cv2
import numpy as np
from testing import get_squares
from piece_square import assign_pieces_to_squares
from ultralytics import YOLO
import json
from piece_square import get_fen_from_board_state
import tkinter as tk
from fen_to_board import ChessboardApp

# Global variables for the board visualization
board_app = None
board_root = None
import time

app = Flask(__name__)
SQUARE_DATA = []

# Model paths
BOARD_MODEL_PATH = os.path.abspath(r"E:\CHESS_OTB\chess\boardfinder.v3i.yolov11\runs\detect\train\weights\best.pt")
PIECE_MODEL_PATH = os.path.abspath(r"E:\CHESS_OTB\otbv5_finetune2\weights\best.pt")

# Pre-load models
try:
    board_model = YOLO(BOARD_MODEL_PATH)
    piece_model = YOLO(PIECE_MODEL_PATH)
    print(f"Models loaded successfully from:\n{BOARD_MODEL_PATH}\n{PIECE_MODEL_PATH}")
except Exception as e:
    print(f"Error loading models: {e}")

@app.route("/detect", methods=["POST"])
def detect():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    
    try:
        
        # Read image from in-memory buffer
        in_memory_file = io.BytesIO()
        file.save(in_memory_file)
        in_memory_file.seek(0)
        file_bytes = np.frombuffer(in_memory_file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({"error": "Could not decode image"}), 400

        # Get squares from the image data using the pre-loaded model
        global SQUARE_DATA
        square_data = get_squares(board_model, image)
        SQUARE_DATA = square_data

        # Annotate image with squares
        for square_name, center in square_data:
            # Draw circle at square center
            cv2.circle(image, center, 5, (0, 0, 255), -1)  # Red dot for square center
            # Draw square name
            cv2.putText(image, square_name, (center[0] - 10, center[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)  # Red text for square name
        
        # Encode the annotated image to a buffer
        _, buffer = cv2.imencode('.jpg', image)
        
        # Convert square data to JSON-serializable format
        json_square_data = []
        for square_name, center in square_data:
            json_square_data.append({
                "square": square_name,
                "center": {"x": int(center[0]), "y": int(center[1])}
            })

        # Save to JSON file
        output_file = "detected_square.json"
        with open(output_file, 'w') as f:
            json.dump(json_square_data, f, indent=2)

        # Prepare the response with both image and square data
        response_data = {
            'squares': json_square_data,
            'image': 'data:image/jpeg;base64,' + base64.b64encode(buffer).decode('utf-8')
        }
        
        return jsonify(response_data)

    except Exception as e:
        app.logger.error(f"Error during detection: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

@app.route("/piece-detect", methods=["POST"])
def piece_detect():
    global SQUARE_DATA  # Declare global at the start of the function
    
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    try:
        # Read image from in-memory buffer
        in_memory_file = io.BytesIO()
        file.save(in_memory_file)
        in_memory_file.seek(0)
        file_bytes = np.frombuffer(in_memory_file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({"error": "Could not decode image"}), 400

        # Detect pieces using the pre-loaded model
        results = piece_model(image)

        # Extract piece data
        piece_data = []
        for result in results:
            for box in result.boxes:
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                if conf > 0.5:  # Confidence threshold
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    center_x = int((x1 + x2) // 2)
                    center_y = int(y2 - (y2 - y1) // 4)
                    piece_type = piece_model.names[cls_id]
                    piece_data.append(((center_x, center_y), piece_type))
                    
                    # Draw detection on image
                    cv2.circle(image, (center_x, center_y), 5, (0, 255, 0), -1)
                    cv2.putText(image, piece_type, (center_x - 20, center_y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        # Get piece positions on the board
        board_state = assign_pieces_to_squares(SQUARE_DATA, piece_data)
        fen = get_fen_from_board_state(board_state)
        print(f"Generated FEN: {fen}")

        # Update the board visualization with the new FEN
        try:
            global board_app, board_root
            if board_app is None or not board_root or not board_root.winfo_exists():
                # Initialize Tkinter window if not exists
                board_root = tk.Tk()
                board_app = ChessboardApp(board_root)
                print("Created new board visualization window")
            
            # Queue the FEN update in the main thread
            board_root.after(0, lambda: board_app.load_fen(fen))
            print(f"FEN update queued successfully: {fen}")
        except Exception as e:
            print(f"Error updating board visualization: {e}")

        # Encode the annotated image to a buffer
        _, buffer = cv2.imencode('.jpg', image)

        # Return both the image and the board state
        response = {
            'board_state': board_state,
            'fen_string': fen,
            'image': 'data:image/jpeg;base64,' + base64.b64encode(buffer).decode('utf-8')
        }

        # Return the response as JSON
        return jsonify(response)

    except Exception as e:
        app.logger.error(f"Error during piece detection: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500



# Enable CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

if __name__ == "__main__":
    # Initialize the board visualization window in a separate thread
    def run_board_window():
        global board_root, board_app
        board_root = tk.Tk()
        board_app = ChessboardApp(board_root)
        board_root.mainloop()

    print("Starting board visualization thread...")
    board_thread = threading.Thread(target=run_board_window, name="BoardThread")
    board_thread.daemon = True  # Make thread exit when main program exits
    board_thread.start()

    # Give the board window time to initialize
    import time
    time.sleep(1)
    
    # Start the Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)

