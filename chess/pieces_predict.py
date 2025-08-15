from ultralytics import YOLO
import os

# Load your trained model
model = YOLO(r"E:\CHESS_OTB\chess\otb.v4i.yolov11\runs\detect\train3\weights\best.pt")

folder_path = r"E:\CHESS_OTB\testimage"

for filename in os.listdir(folder_path):
    full_path = os.path.join(folder_path, filename)

    # Run inference
    results = model(full_path)  # returns a list of Results objects

    # Process each detection result
    for result in results:
        boxes = result.boxes      # bounding boxes
        masks = result.masks      # segmentation masks (if available)
        keypoints = result.keypoints
        probs = result.probs
        obb = result.obb

        # Show result in a window
        result.show()

        # Save result image with detections
        save_path = os.path.join(folder_path, f"out_{filename}")
        result.save(filename=save_path)

        print(f"Processed {filename}, saved to {save_path}")
