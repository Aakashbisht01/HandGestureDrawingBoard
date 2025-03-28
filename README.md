# HandGestureDrawingBoard
 Hand Gesture Drawing Board is an interactive virtual drawing application that allows users to draw on a digital canvas using only their hand gestures. Using OpenCV and MediaPipe, the system detects hand movements and translates them into drawing actions such as drawing, erasing, changing colors, and clearing the canvas.

Hand Gesture Drawing Board 🎨✋
A real-time drawing application using hand gestures and computer vision powered by Flask, OpenCV, and MediaPipe. This project allows users to draw on a virtual canvas using hand gestures, without touching the screen.

(Replace with an actual image/GIF)

📌 Features
✅ Draw using hand gestures
✅ Erase drawings with a gesture
✅ Change colors dynamically
✅ Real-time video streaming
✅ Simple and interactive UI

🛠️ Technologies Used
Python (Flask for the web server)

OpenCV (for video processing)

MediaPipe (for hand tracking)

HTML, CSS, JavaScript (for the frontend)

🚀 Installation & Setup
🔹 1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/Aakashbisht01/HandGestureDrawingBoard.git
cd HandGestureDrawingBoard
🔹 2. Create a Virtual Environment (Recommended)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # For Mac/Linux
venv\Scripts\activate      # For Windows
🔹 3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
🔹 4. Run the Flask Application
bash
Copy
Edit
python app.py
Open your browser and go to http://127.0.0.1:5000/ to start drawing!

📸 Usage Instructions
🖐️ Gesture Controls:

Thumb + Index Finger Close → Start drawing

Thumb + Index Finger Apart → Stop drawing

Close All Fingers → Clear Canvas

Pinky Finger Close to Thumb → Toggle Eraser

Thumb + Middle Finger → Change Color

