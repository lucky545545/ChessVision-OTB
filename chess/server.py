import os, io, base64
from flask import Flask, request, send_file, jsonify
import cv2
import numpy as np
from testing import get_squares
from piece_square import assign_pieces_to_squares
from ultralytics import YOLO
import json
app = Flask(__name__)
SQUARE_DATA = []

# Model paths
BOARD_MODEL_PATH = os.path.abspath(r"E:\CHESS_OTB\chess\boardfinder.v3i.yolov11\runs\detect\train\weights\best.pt")
PIECE_MODEL_PATH = os.path.abspath(r"E:\CHESS_OTB\chess\otb.v4i.yolov11\runs\detect\train3\weights\best.pt")

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

        # Annotate image
        for square_name, center in square_data:
            x, y = center
            cv2.circle(image, (int(x), int(y)), 5, (0, 0, 255), -1)
            cv2.putText(image, square_name, (int(x) - 15, int(y) - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Encode the annotated image to a buffer
        _, buffer = cv2.imencode('.jpg', image)
        
        output_file = "detected_square.json"
        with open(output_file, 'w') as f:
            json.dump(square_data, f)

        # Send the buffer as a response
        return send_file(
            io.BytesIO(buffer),
            mimetype='image/jpeg',
            as_attachment=False,
            download_name='result.jpg'
        )

        

    except Exception as e:
        app.logger.error(f"Error during detection: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

@app.route("/piece-detect", methods=["POST"])
def piece_detect():
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
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    piece_type = piece_model.names[cls_id]
                    piece_data.append(((center_x, center_y), piece_type))
                    
                    # Draw detection on image
                    cv2.circle(image, (center_x, center_y), 5, (0, 255, 0), -1)
                    cv2.putText(image, piece_type, (center_x - 20, center_y - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.imshow("Detected Chess Pieces", image) 
        cv2.waitKey(0) 
        cv2.destroyAllWindows()

        # Get piece positions on the board
        board_state = assign_pieces_to_squares(piece_data, SQUARE_DATA)

        # Encode the annotated image to a buffer
        _, buffer = cv2.imencode('.jpg', image)
        
        # Return both the image and the board state
        response = {
            'board_state': board_state,
            'image': 'data:image/jpeg;base64,' + base64.b64encode(buffer).decode('utf-8')
        }

        # Return the response as JSON
        return jsonify(piece_data)

    except Exception as e:
        app.logger.error(f"Error during piece detection: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500



# Enable CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
