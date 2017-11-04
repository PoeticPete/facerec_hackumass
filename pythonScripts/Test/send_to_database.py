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
picture_path = "zebra.png"

def send_frame_to_database(picture_path, name):
    
    random_key = db.generate_key()

    storage.child("images/" + random_key).put(picture_path)
    url = storage.child("images/" + random_key).get_url(None)

    upload_dict = {"name": name, "timestamp":{".sv": "timestamp"}, "photoURL": url}
    db.child("oolala").child(db.generate_key()).set(upload_dict)


send_frame_to_database(picture_path, name)
