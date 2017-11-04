import face_recognition             # facial recognition module
import pyrebase                     # connect with Firebase
import threading                    # run on background thread
import urllib.request               # get image from web

# configure firebase
config = {
    "apiKey": "AIzaSyC3tcDJPD4nXPslkhZ7gscE8p9Im4Gw00s",
    "authDomain": "easy-lock.firebaseapp.com",
      "databaseURL": "https://easy-lock.firebaseio.com/",
      "storageBucket": "easy-lock.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()

names = []

# store face encodings in an array
known_encodings = []


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []



'''
    FUNCTION: sends a picture to the storage bucket and makes a post to the database
'''
def send_frame_to_database(key, picture_path, name):

    storage.child("images/" + key).put(picture_path)
    url = storage.child("images/" + key).get_url(None)

    upload_dict = {"name": name, "timestamp":{".sv": "timestamp"}, "photoURL": url}
    db.child("savedFrames/door1").child(key).set(upload_dict)

'''
    FUNCTION: handles the real time firebase data stream. When a new photo is added to the database, it is synced in real time with this computer.
'''
def stream_handler(message):
    print("got a message")
    print(message["event"]) # put
    print(message["path"]) # /-K7yGTTEp7O549EzTYtI

    if message["data"]:
        file_name = "faces/"
        data = message["data"]
#        print(data)

        #  Make sure the data being retrieved is a dictionary
        if type(data) is dict:

            #  If the data returned is a single item
            if "mediaURL" in data:
#                print("SINGLE ITEM")
                mediaURL = str(data["mediaURL"])
                name = str(data["name"])
#                print(mediaURL, name)
                urllib.request.urlretrieve(mediaURL, file_name + name)
                names.append(name)
                known_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(file_name + name))[0])

            #  If the data returned is a a list of items
            else:
                print("MULTIPLE ITEMS")

                for key,value in data.items():
                    mediaURL = str(value["mediaURL"])
                    name = str(value["name"])
                    print(mediaURL, name)
                    urllib.request.urlretrieve(mediaURL, file_name + name)
                    try:
                        tmp = face_recognition.face_encodings(face_recognition.load_image_file(file_name + name))[0]
                        known_encodings.append(tmp)
                        names.append(name)
                    except:
                        print("Couldn't find a face for " + name + "!!! Crap...")
        else:
            print("data is not a dictttt")
    else:
        print("NO DATA LOL")


'''
    FUNCTION: starts the stream at the given database location, and handles the stream with the stream_handler function
'''
class FirebaseStreamer(threading.Thread):
   def __init__(self, threadID, ):
      threading.Thread.__init__(self)
      self.threadID = threadID
   def run(self):
      startStream()

def startStream():
    db.child("people/door1").stream(stream_handler)


# start stream on another thread so the camera can run on main thread
firebaseThread = FirebaseStreamer("FirebaseStreamer")
firebaseThread.start()
