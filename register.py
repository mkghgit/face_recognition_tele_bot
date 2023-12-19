import cv2
import face_recognition
import os


def face_reg(user_id) -> bool:
    photo = face_recognition.load_image_file(
        r'database\photos\{}\file.jpg'.format(user_id))
    face_locations = face_recognition.face_locations(photo)
    if face_locations:
        top, right, bottom, left = face_locations[0]
        face_image = photo[top:bottom, left:right]
        os.makedirs(f"database/{user_id}", exist_ok=True)
        cv2.imwrite(os.path.join(
            f"database/{user_id}", f"person_{str(user_id)}.jpg"), face_image)
        print(f"Person {user_id} captured!")

        cv2.imwrite(os.path.join(f"database/faces/",
                    f"{str(user_id)}.jpg"), face_image)
        return True
    else:
        print("Это не ебало")
        return False
