import cv2
import time
import uuid
import pyrebase

config = {
    "apiKey": "AIzaSyDoGaO58eRibD1--3xVXLJz9a4o_Xfnv3s",
    "authDomain": "hacking-for-gooooooood.firebaseapp.com",
    "databaseURL": "https://hacking-for-gooooooood.firebaseio.com/",
    "storageBucket": "hacking-for-gooooooood.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()

name = "Lynn something something"


def send_frame_to_database(key, picture_path, name):
    
    storage.child("images/" + key).put(picture_path)
    url = storage.child("images/" + key).get_url(None)
    
    upload_dict = {"name": name, "timestamp":{".sv": "timestamp"}, "photoURL": url}
    db.child("savedFrames").child(key).set(upload_dict)


def save_frame(filepath, frame):
    cv2.imwrite(filepath, frame)


video_capture = cv2.VideoCapture(0)
while True:
    random_key = db.generate_key()
    ret, frame = video_capture.read()
    cv2.imshow('Video', frame)
    save_frame("saved_frames/" + random_key + ".jpg", frame)
    time.sleep(10)
    send_frame_to_database(random_key, "saved_frames/" + random_key + ".jpg", name)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break








