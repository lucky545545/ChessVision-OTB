def pieces_to_fen(piece_list):
    # Map piece names to FEN symbols
    piece_map = {
        'WhiteKing': 'K', 'WhiteQueen': 'Q', 'WhiteRook': 'R',
        'WhiteBishop': 'B', 'WhiteKnight': 'N', 'WhitePawn': 'P',
        'BlackKing': 'k', 'BlackQueen': 'q', 'BlackRook': 'r',
        'BlackBishop': 'b', 'BlackKnight': 'n', 'BlackPawn': 'p'
    }

    # Create empty 8x8 board
    board = [['' for _ in range(8)] for _ in range(8)]

    # Place pieces
    for piece, square in piece_list:
        file = ord(square[0].lower()) - ord('a')  # 0-7
        rank = 8 - int(square[1])  # rank 8 at row 0
        board[rank][file] = piece_map[piece]

    # Convert board to FEN
    fen_rows = []
    for row in board:
        empty_count = 0
        fen_row = ''
        for cell in row:
            if cell == '':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += cell
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)

    fen_position = '/'.join(fen_rows)

    # Append default FEN extras (active color, castling, en passant, halfmove, fullmove)
    fen = f"{fen_position} w - - 0 1"
    return fen


# Example usage
piece_list = [
    ('BlackRook', 'D6'), ('WhiteQueen', 'F2'), ('BlackPawn', 'G7'),
    ('BlackKnight', 'C5'), ('WhiteRook', 'H1'), ('WhiteKing', 'E1'),
    ('BlackKing', 'E8'), ('WhiteBishop', 'E1')
]

print(pieces_to_fen(piece_list))
