import tkinter as tk
from tkinter import font, messagebox

class ChessboardApp:
    """
    A Tkinter application that displays a chessboard and updates the position
    based on a FEN (Forsyth-Edwards Notation) string provided by the user.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("FEN Chessboard Viewer")
        self.root.geometry("600x700")
        self.root.configure(bg="#312e2b") # A dark, pleasant background

        # --- Constants and State Variables ---
        self.square_size = 70
        self.board_size = 8 * self.square_size
        self.colors = ("#f0d9b5", "#b58863")  # Light, Dark square colors
        self.start_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        
        # Unicode characters for chess pieces
        self.piece_map = {
            'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚',
            'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔'
        }

        # --- UI Setup ---
        self.main_frame = tk.Frame(root, bg="#312e2b")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- FEN Input Controls ---
        self._setup_fen_controls()

        # --- Chessboard Canvas ---
        self.canvas = tk.Canvas(
            self.main_frame, 
            width=self.board_size, 
            height=self.board_size, 
            borderwidth=0, 
            highlightthickness=0
        )
        self.canvas.pack(pady=20)
        
        # Use a font that supports unicode chess pieces well
        self.piece_font = font.Font(family='Segoe UI Symbol', size=38)
        
        # --- Initial Board Setup ---
        self.draw_board_squares()
        self.load_fen(self.start_fen)

    def _setup_fen_controls(self):
        """Creates and packs the FEN input and display widgets."""
        fen_frame = tk.Frame(self.main_frame, bg="#4a4643", relief=tk.RIDGE, borderwidth=2)
        fen_frame.pack(pady=(10, 20), padx=10, fill=tk.X)

        self.fen_input_var = tk.StringVar(value=self.start_fen)
        fen_input = tk.Entry(
            fen_frame, 
            textvariable=self.fen_input_var, 
            font=("Courier New", 12), 
            bg="#312e2b", 
            fg="white", 
            insertbackground="white", 
            borderwidth=2, 
            relief=tk.FLAT
        )
        fen_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)

        set_fen_button = tk.Button(
            fen_frame, 
            text="Update Board", 
            command=self.apply_fen_from_input, 
            font=("Arial", 10, "bold"), 
            bg="#769656", 
            fg="white", 
            activebackground="#8fbc8f", 
            relief=tk.FLAT, 
            borderwidth=0, 
            padx=10
        )
        set_fen_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def draw_board_squares(self):
        """Draws the 64 squares of the chessboard grid."""
        for row in range(8):
            for col in range(8):
                x1, y1 = col * self.square_size, row * self.square_size
                x2, y2 = x1 + self.square_size, y1 + self.square_size
                color = self.colors[(row + col) % 2]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def load_fen(self, fen):
        """
        Clears the board and renders a new position based on a FEN string.
        This is the core logic for updating the view.
        """
        # Clear only the pieces, not the board squares
        self.canvas.delete("piece")
        
        try:
            # 1. Parse the piece placement part of the FEN
            piece_placement = fen.split(' ')[0]
            ranks = piece_placement.split('/')
            
            # 2. Iterate over each rank (row)
            for rank_idx, rank_str in enumerate(ranks):
                file_idx = 0 # Represents the column
                # 3. Iterate over each character in the rank string
                for char in rank_str:
                    if char.isdigit():
                        # If it's a number, skip that many columns
                        file_idx += int(char)
                    else:
                        # If it's a piece, place it on the board
                        if 0 <= rank_idx < 8 and 0 <= file_idx < 8:
                            x = file_idx * self.square_size + self.square_size / 2
                            y = rank_idx * self.square_size + self.square_size / 2
                            
                            piece_symbol = self.piece_map.get(char, '?')
                            color = "white" if char.isupper() else "black"
                            
                            # Create the text item with a "piece" tag for easy deletion
                            self.canvas.create_text(
                                x, y, text=piece_symbol, 
                                font=self.piece_font,
                                tags="piece", 
                                fill=color
                            )
                        file_idx += 1
        except Exception as e:
            messagebox.showerror("FEN Error", f"Invalid or malformed FEN string.\n\nDetails: {e}")

    def apply_fen_from_input(self):
        """Command for the button to apply the FEN from the input box."""
        fen = self.fen_input_var.get().strip()
        if fen:
            self.load_fen(fen)
        else:
            messagebox.showwarning("Input Error", "FEN string cannot be empty.")

# --- Main execution block ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ChessboardApp(root)
    root.mainloop()

