import face_recognition             # facial recognition module
import cv2                          # capture frames from webcam
import pyrebase                     # connect with Firebase
import threading                    # run firebase stream on background thread
import time                         # get current time
import firebase_helper              # Firebase helper module
import notification_helper          # Notification helper module


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
video_capture.set(3,7680)
video_capture.set(4,4320)
scaling_factor = 4    # scale down the captured image by this much for efficiency


def getColor(name):
    '''
    Return the color of the rectangle to be drawn around a face.
    Unknown should have a red rectangle.
    Known faces should have a green rectangle.
    '''
    if name == "Unknown":
        return(0,0,255)
    else:
        return(0,255,0)


def attemptToOpenDoor(name):
    '''
    Attempt to open door with a name. If name is not unknown, the door should
    open.
    '''
    firebase_helper.lock.acquire()
    print('READ firebase_helper.is_locked=', str(firebase_helper.is_locked))

    if name != "Unknown" and firebase_helper.is_locked:
        print("unlocking!")
        firebase_helper.db.child("doors/door1").update({"status": False, "lastChanged":{".sv": "timestamp"}})
    else:
        print("not unlocking!" + str(firebase_helper.is_locked))

    firebase_helper.lock.release()

# counter used to process only certain frames
counter = 0

# start the camera stream on the main thread
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=1.0/scaling_factor, fy=1.0/scaling_factor)

    # Only process one of every 10 frames of video to save
    if counter % 2 == 0:
        # Find all the faces and face encodings in the current frame of video
        firebase_helper.face_locations = face_recognition.face_locations(small_frame)
        firebase_helper.face_encodings = face_recognition.face_encodings(small_frame, firebase_helper.face_locations)

        firebase_helper.face_names = []
        for face_encoding in firebase_helper.face_encodings:
            # See if the face is a match for the known face(s)
            match = list(face_recognition.face_distance(firebase_helper.known_encodings, face_encoding))
            name = "Unknown"
            best_match_dist = 1
            for i in range(len(match)):
                if match[i] < best_match_dist and match[i] < .55:
                    best_match_dist = match[i]
                    name = firebase_helper.names[i]
                    attemptToOpenDoor(name)

            if notification_helper.should_send_notification(name):
                notification_helper.last_sent_notifications[name] = time.time()
                random_key = firebase_helper.db.generate_key()
                notification_helper.notificationQueue.append((frame, name, random_key))

            firebase_helper.face_names.append(name)
        counter = 0
    counter += 1

    # Display the results
    for (top, right, bottom, left), name in zip(firebase_helper.face_locations, firebase_helper.face_names):
        # Scale back up face locations since the frame we detected in was scaled
        top *= scaling_factor
        right *= scaling_factor
        bottom *= scaling_factor
        left *= scaling_factor

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), getColor(name), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), getColor(name), -1)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)


    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
