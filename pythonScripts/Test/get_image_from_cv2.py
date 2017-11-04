import cv2
import time
import uuid



video_capture = cv2.VideoCapture(0)
def save_frame(filepath, frame):
    cv2.imwrite(filepath, frame)

while True:
    ret, frame = video_capture.read()
    cv2.imshow('Video', frame)
    save_frame("saved_frames/" + str(uuid.uuid4()) + ".jpg", frame)
    time.sleep(1)
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



#cap = cv2.VideoCapture(0)
#time.sleep(0.5)
#_,frame = cap.read()
#cv2.imwrite("saved_frames/got from cv2.jpg", frame)

