
import face_recognition
import os
import cv2
import numpy as np
import json
images_folder = "database/faces"
def yebalo_detect(user_id):
    # Function to load face images and IDs
    def load_face_images_and_ids(folder):
        face_images = []
        person_ids = []

        for filename in os.listdir(folder):
            if filename.endswith(".jpg"):
                path = os.path.join(folder, filename)
                face_image = face_recognition.load_image_file(path)
                face_encoding = face_recognition.face_encodings(face_image)[0]
                person_id = int(os.path.splitext(filename)[0].split('_')[0])
                face_images.append(face_encoding)
                person_ids.append(person_id)
        return np.array(face_images), np.array(person_ids)
    known_face_encodings, known_person_ids = load_face_images_and_ids(images_folder)

    cap = cv2.imread(f"database/chek_face/{user_id}/file.jpg")
    frame = cap

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        person_id = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            person_id = known_person_ids[first_match_index]
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        with open(f"database/{user_id}/info.json", "r") as json_file:
            json_file.read()
        cv2.putText(frame, f"Person ID: {person_id}", (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Display the image
    # cv2.imshow('Face Recognition', frame)
    # Wait for a key press to exit
    # cv2.waitKey(0)
    # Save the image to a file
    os.makedirs(f"database/saved_jpgs/{user_id}", exist_ok=True)
    cv2.imwrite(f"database/saved_jpgs/{user_id}.jpg", frame)


