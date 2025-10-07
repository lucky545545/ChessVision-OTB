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
def get_fen_from_board_state(board_state):
    """
    Converts the board state into a FEN string.
    
    Args:
        board_state: List of (square_name, piece_type) tuples
    
    Returns:
        FEN string representing the board state
    """
    # Map piece types to FEN characters
    piece_to_fen = {
    'WhitePawn': 'P', 'WhiteRook': 'R', 'WhiteKnight': 'N',
    'WhiteBishop': 'B', 'WhiteQueen': 'Q', 'WhiteKing': 'K',
    'BlackPawn': 'p', 'BlackRook': 'r', 'BlackKnight': 'n',
    'BlackBishop': 'b', 'BlackQueen': 'q', 'BlackKing': 'k'
}
    
    # Initialize empty board
    fen_rows = []
    for rank in range(8, 0, -1):
        fen_row = ''
        empty_count = 0
        for file in 'ABCDEFGH':
            square_name = f"{file}{rank}"
            piece_type = next((ptype for sq_name, ptype in board_state if sq_name == square_name), None)
            if piece_type:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += piece_to_fen.get(piece_type, '?')
            else:
                empty_count += 1
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)
    
    fen_string = '/'.join(fen_rows) + " w KQkq - 0 1"  
    return fen_string
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