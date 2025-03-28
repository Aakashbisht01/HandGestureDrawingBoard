from flask import Flask, Response, render_template
import cv2
import numpy as np
import mediapipe as mp
import random

app = Flask(__name__)

# Mediapipe and OpenCV setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Canvas settings
canvas = None
pencil_color = (0, 0, 255)  # Red
pencil_size = 5
background_color = (255, 255, 255)  # White
drawing = False
current_tool = 'pencil'

# Utility functions
def distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return int(np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2))

def random_color():
    """Generate a random color."""
    return tuple(random.randint(0, 255) for _ in range(3))

def toggle_tool():
    """Switch between pencil and eraser."""
    global current_tool, pencil_color, pencil_size
    if current_tool == 'pencil':
        current_tool = 'eraser'
        pencil_color = background_color
        pencil_size = 30
    else:
        current_tool = 'pencil'
        pencil_color = (0, 0, 255)
        pencil_size = 5

# Video processing function
def process_video():
    global canvas, drawing, current_tool, pencil_color, pencil_size
    cap = cv2.VideoCapture(0)
    prev_x, prev_y = None, None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        if canvas is None:
            canvas = np.ones_like(frame) * 255

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = hand_landmarks.landmark
                height, width, _ = frame.shape

                thumb_tip = (int(landmarks[4].x * width), int(landmarks[4].y * height))
                index_tip = (int(landmarks[8].x * width), int(landmarks[8].y * height))
                middle_tip = (int(landmarks[12].x * width), int(landmarks[12].y * height))
                pinky_tip = (int(landmarks[20].x * width), int(landmarks[20].y * height))

                thumb_to_index = distance(thumb_tip, index_tip)
                thumb_to_pinky = distance(thumb_tip, pinky_tip)

                if thumb_to_index < 50 and thumb_to_pinky > 100:
                    drawing = True
                elif thumb_to_index > 100 and thumb_to_pinky > 100:
                    drawing = False
                elif thumb_to_index < 50 and thumb_to_pinky < 50:
                    canvas = np.ones_like(frame) * 255
                elif thumb_to_pinky < 50 and thumb_to_index > 50:
                    toggle_tool()
                elif thumb_to_index < 50 and middle_tip[1] > index_tip[1]:
                    pencil_color = random_color()

                if drawing and current_tool == 'pencil':
                    if prev_x is not None and prev_y is not None:
                        cv2.line(canvas, (prev_x, prev_y), index_tip, pencil_color, pencil_size)
                    prev_x, prev_y = index_tip
                else:
                    prev_x, prev_y = None, None

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        combined = cv2.addWeighted(frame, 0.5, canvas.astype(np.uint8), 0.5, 0)

        # Encode the frame for streaming
        _, buffer = cv2.imencode('.jpg', combined)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(process_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
