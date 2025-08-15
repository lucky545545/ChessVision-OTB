import os, json
import io
from flask import Flask, request, send_file, jsonify
import cv2
import numpy as np
from testing import get_squares, get_pieces

app = Flask(__name__)

# absolute model paths
BOARD_MODEL_PATH   = r"E:\CHESS_OTB\chess\boardfinder.v3i.yolov11\runs\detect\train\weights\best.pt"
PIECES_MODEL_PATH  = r"E:\CHESS_OTB\chess\otb.v4i.yolov11\runs\detect\train3\weights\best.pt"

TARGET_CLASS      = "square"
EXPECTED_SQUARES  = 64

@app.route("/detect", methods=["POST"])
def detect():
    clock_side = "right_w"
    file = request.files.get("image")

    if not file:
        return jsonify({"error": "No image uploaded"}), 400

    # Read the image from memory (no temp file)
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image is None:
        return jsonify({"error": "Invalid image"}), 400

    # Run your detection directly on the in-memory image
    # If get_squares expects a path, we need to modify it to accept an image array.
    square_data = get_squares(BOARD_MODEL_PATH, image, TARGET_CLASS, EXPECTED_SQUARES, clock_side)

    # Annotate detections
    for square_name, center in square_data:
        x, y = center
        cv2.circle(image, (int(x), int(y)), 5, (0, 0, 255), -1)
        cv2.putText(image, square_name, (int(x) - 15, int(y) - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.putText(image, f"Squares: {len(square_data)}/64", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if request.args.get("format") == "json":
        return jsonify({
            "squares": [
                {"name": name, "center": [int(x), int(y)]}
                for name, (x, y) in square_data
            ]
        })
    else:
        # Encode image to JPEG in memory and return
        _, buffer = cv2.imencode(".jpg", image)
        return send_file(
            io.BytesIO(buffer),
            mimetype="image/jpeg",
            as_attachment=False,
            download_name="result.jpg"
        )

if __name__ == "__main__":
    app.run(debug=True)
