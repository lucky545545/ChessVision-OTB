# ChessVision-OTB (Over The Board)

A computer vision-based chess position recognition system that can detect chess pieces and boards from real-world photos and convert them into digital chess positions.
<p align="center">
  <a href="https://www.youtube.com/watch?v=5n3iaH3oFlc" target="_blank">
    <img src="./demo/video_thumbnail.png" alt="Watch the Video Demo" width="400"/>
  </a>
</p>
## Features

- Real-time chess board square detection
- Accurate piece recognition and classification
- FEN string generation from detected positions
- Interactive board visualization
- Mobile app integration
- Cross-platform compatibility

## System Components

### 1. Computer Vision Models
- **Board Detection**: YOLO model trained for chess board square detection
- **Piece Detection**: YOLO model trained for chess piece classification
- Models located in:
  - `chess/boardfinder.v3i.yolov11/` (board detection)
  - `otb.v4i.yolov11/` (piece detection)

### 2. Backend Server (Flask)
Located in `chess/server.py`, provides:
- REST API endpoints for image processing
- Board detection endpoint (`/detect`)
- Piece detection endpoint (`/piece-detect`)
- FEN string generation
- Real-time board visualization updates

### 3. Board Visualization (Tkinter)
Located in `chess/fen_to_board.py`:
- Interactive chessboard display
- FEN string parsing and rendering
- Real-time position updates
- Chess piece unicode rendering

### 4. Mobile Application (React Native)
Located in `ChessVision/`:
- Camera integration for capturing chess positions
- Real-time board detection
- Communication with backend server
- Position visualization

## Technical Stack

- **Backend**: Python, Flask
- **Computer Vision**: YOLO, OpenCV
- **Frontend**: React Native, Expo
- **Visualization**: Tkinter
- **Mobile**: React Native, Expo Camera

## Installation

1. Clone the repository:
```bash
git clone https://github.com/lucky545545/ChessVision-OTB.git
cd ChessVision-OTB
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install mobile app dependencies:
```bash
cd ChessVision
npm install
```

## Usage

### Starting the Backend Server

1. Navigate to the chess directory:
```bash
cd chess
```

2. Start the Flask server:
```bash
python server.py
```

The server will start on `http://0.0.0.0:5000`

### Running the Mobile App

1. Navigate to the ChessVision directory:
```bash
cd ChessVision
```

2. Start the Expo development server:
```bash
npx expo start
```

3. Use the Expo Go app to run the application on your mobile device

## Model Structure

### Board Detection
- Model: YOLOv11
- Target: Chess board squares
- Output: 64 square coordinates with chess notation (A1-H8)

### Piece Detection
- Model: YOLOv11
- Target: Chess pieces (12 classes)
- Classes: White/Black {Pawn, Rook, Knight, Bishop, Queen, King}

## API Endpoints

### `/detect` (POST)
- Input: Chess board image
- Output: Square coordinates and annotated image

### `/piece-detect` (POST)
- Input: Chess board image with pieces
- Output: 
  - Piece positions
  - FEN string
  - Annotated image

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- YOLOv11 for object detection
- OpenCV for image processing
- React Native and Expo for mobile development
- Flask for backend services
