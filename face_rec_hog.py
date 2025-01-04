import cv2
import face_recognition
import os
import pickle
import time

def recognize_or_register_face():
    """
    Captures a frame from the webcam, recognizes the face if it's known,
    and returns the user's name. If the face is unrecognized, prompts for
    the user's name, registers the face, and saves it for future use.
    
    Processes the image for at least 3 seconds before naming the user.

    Returns:
        str: The name of the recognized or newly registered user.
    """

    # Helper functions to handle face encodings
    def load_face_encodings():
        if os.path.exists('known_faces.pkl') and os.path.getsize('known_faces.pkl') > 0:
            with open('known_faces.pkl', 'rb') as f:
                return pickle.load(f)
        return [], []

    def save_face_encodings(encodings, names):
        with open('known_faces.pkl', 'wb') as f:
            pickle.dump((encodings, names), f)

    # Initialize the webcam
    video_capture = cv2.VideoCapture(0)

    # Load known face encodings and names
    known_face_encodings, known_face_names = load_face_encodings()

    # Capture a single frame from the webcam
    start_time = time.time()
    while time.time() - start_time < 3:
        ret, frame = video_capture.read()
        if not ret:
            break

    # Release the webcam
    video_capture.release()

    # If the frame couldn't be captured, return None
    if not ret:
        return None

    # Find all face locations and face encodings in the frame
    face_locations = face_recognition.face_locations(frame, model="hog")
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding in face_encodings:
        # Check if the face matches any known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
        name = "Unknown"

        if True in matches:
            # Get the name of the first matching face
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        else:
            # If the face is not recognized, register it
            print("New face detected! Please enter your name:")
            name = input("Name: ").strip()

            # Add the new face encoding and name to the known faces database
            known_face_encodings.append(face_encoding)
            known_face_names.append(name)

            # Save the updated face encodings and names
            save_face_encodings(known_face_encodings, known_face_names)

        return name

    # If no faces were detected, return None
    return None

