import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, render_template, Response, jsonify

app = Flask(_name_)

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

blink_detected = False
face_detected = False
blink_ready = False
previous_landmarks = None
movement_threshold = 0.01  # Define movement threshold to detect real face

# Function to calculate Eye Aspect Ratio (EAR)
def calculate_ear(eye):
    A = np.linalg.norm(np.array([eye[1].x, eye[1].y]) - np.array([eye[5].x, eye[5].y]))
    B = np.linalg.norm(np.array([eye[2].x, eye[2].y]) - np.array([eye[4].x, eye[4].y]))
    C = np.linalg.norm(np.array([eye[0].x, eye[0].y]) - np.array([eye[3].x, eye[3].y]))
    ear = (A + B) / (2.0 * C)
    return ear

# Function to detect blink and ensure the face is real (not a photo)
def detect_blink_and_real_face(landmarks):
    global blink_detected, face_detected, blink_ready, previous_landmarks

    # Indices for left and right eye landmarks (from MediaPipe FaceMesh)
    left_eye_indices = [33, 160, 158, 133, 153, 144]
    right_eye_indices = [362, 385, 387, 263, 373, 380]

    # Extract landmarks for left and right eyes
    left_eye_landmarks = [landmarks[i] for i in left_eye_indices]
    right_eye_landmarks = [landmarks[i] for i in right_eye_indices]

    # Calculate EAR for both eyes
    left_eye_ear = calculate_ear(left_eye_landmarks)
    right_eye_ear = calculate_ear(right_eye_landmarks)

    # Blink detection threshold
    blink_threshold = 0.25

    # If the EAR falls below threshold, we detect a blink (eyes closed)
    if left_eye_ear < blink_threshold and right_eye_ear < blink_threshold:
        blink_ready = True  # Blink is ready when eyes are closed
    elif blink_ready and left_eye_ear > blink_threshold and right_eye_ear > blink_threshold:
        # Once the eyes are open again after a blink, check for real movement
        if detect_real_face_movement(landmarks):
            blink_ready = False
            blink_detected = True
            face_detected = True
    return face_detected

# Function to detect real movement by comparing previous and current landmarks
def detect_real_face_movement(landmarks):
    global previous_landmarks, movement_threshold

    if previous_landmarks is None:
        previous_landmarks = landmarks
        return False  # No movement detected for the first frame

    total_movement = 0
    num_landmarks = len(landmarks)

    # Compare current landmarks with previous landmarks
    for i in range(num_landmarks):
        movement = np.linalg.norm(np.array([landmarks[i].x, landmarks[i].y]) - np.array([previous_landmarks[i].x, previous_landmarks[i].y]))
        total_movement += movement

    # Calculate the average movement across landmarks
    average_movement = total_movement / num_landmarks

    # Update the previous landmarks
    previous_landmarks = landmarks

    # If the average movement is greater than the threshold, it's a real face
    if average_movement > movement_threshold:
        return True  # Real movement detected
    return False  # No real movement detected

# Generate frames from the webcam
def generate_frames():
    global blink_detected, face_detected

    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)

        if not face_detected:
            # Convert frame to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = face_mesh.process(rgb_frame)

            if result.multi_face_landmarks:
                for face_landmarks in result.multi_face_landmarks:
                    # Detect blink and ensure it's a real face
                    detect_blink_and_real_face(face_landmarks.landmark)

                    if face_detected:
                        cv2.putText(frame, 'Face Detected After Blink', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                        break
                    else:
                        cv2.putText(frame, 'Blink to Detect Real Face', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, 'No Face Detected', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, 'Face Detected After Blink', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Encode the frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/retry')
def retry():
    global blink_detected, face_detected
    blink_detected = False
    face_detected = False
    return jsonify(success=True)

if _name_ == '_main_':
    app.run(debug=True)