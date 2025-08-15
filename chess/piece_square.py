from testing import get_pieces
from testing import get_squares
import numpy as np
from scipy.spatial import KDTree   
# Use the function
square_data = get_squares(r"E:\CHESS_OTB\chess\boardfinder.v3i.yolov11\runs\detect\train\weights\best.pt",
                              r"E:\CHESS_OTB\chess\new_img.jpg" )
piece_data = get_pieces(
    r"E:\CHESS_OTB\chess\otb.v4i.yolov11\runs\detect\train3\weights\best.pt",
    r"E:\CHESS_OTB\chess\new_img_w_pieces.jpg"
)
print("Imported squares:")
for square_name, center in square_data:
    print(f"square_name: {square_name}, at Center: {center}") 
print("Imported detections:")
for center, piece_type in piece_data:
    print(f"{piece_type} at {center}")


def assign_pieces_to_squares(squares, pieces):
    """
    squares: [(sq_name, (sx, sy)), ...]   len == 64
    pieces : [(piece,   (px, py)), ...]

    returns: [(piece, closest_sq_name), ...]
    """
    # 1. Build k-d tree on square centers
    sq_centers = np.array([(int(x), int(y)) for _, (x, y) in squares],
                          dtype=np.int32)
    tree = KDTree(sq_centers)

    # 2. Query nearest square for every piece
    out = []
    sq_names = [name for name, _ in squares]   # keep order
    for (px, py) , piece in pieces:
        _, idx = tree.query((int(px), int(py)))
        out.append((piece, sq_names[idx]))
    return out


print(assign_pieces_to_squares(square_data, piece_data))