from testing import get_pieces, get_squares
import numpy as np
from scipy.spatial import KDTree
from ultralytics import YOLO

def load_models():
    """Load YOLO models for board and piece detection."""
    board_model = YOLO(r"E:\CHESS_OTB\chess\boardfinder.v3i.yolov11\runs\detect\train\weights\best.pt")
    piece_model = YOLO(r"E:\CHESS_OTB\chess\otb.v4i.yolov11\runs\detect\train3\weights\best.pt")
    return board_model, piece_model

def assign_pieces_to_squares(squares, pieces):
    """
    Assigns detected pieces to their closest squares using KD-tree for efficient nearest neighbor search.
    
    Args:
        squares: List of (square_name, (x, y)) tuples
        pieces: List of ((x, y), piece_type) tuples
    
    Returns:
        List of (square_name, piece_type) tuples representing the board state
    """
    # 1. Build k-d tree on square centers
    sq_centers = np.array([(int(x), int(y)) for _, (x, y) in squares],
                          dtype=np.int32)
    tree = KDTree(sq_centers)

    # 2. Query nearest square for every piece
    assignments = {}  # square_name -> piece_type
    sq_names = [name for name, _ in squares]   # keep order
    
    for (px, py), piece_type in pieces:
        _, idx = tree.query((int(px), int(py)))
        assignments[sq_names[idx]] = piece_type

    # 3. Create the final board state
    board_state = []
    for square_name, _ in squares:
        piece_type = assignments.get(square_name, None)
        board_state.append((square_name, piece_type))
    
    return board_state

def get_board_state(image_path):
    """Get the current state of the chess board from an image."""
    board_model, piece_model = load_models()
    square_data = get_squares(board_model, image_path)
    piece_data = get_pieces(piece_model, image_path)
    return assign_pieces_to_squares(square_data, piece_data)

if __name__ == "__main__":
    # Example usage
    image_path = r"E:\CHESS_OTB\chess\new_img_w_pieces.jpg"
    board_state = get_board_state(image_path)
    print("Board state:")
    for square_name, piece_type in board_state:
        if piece_type:  # Only print squares with pieces
            print(f"{piece_type} at {square_name}")