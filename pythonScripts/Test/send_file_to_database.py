import pyrebase


config = {
    "apiKey": "AIzaSyDoGaO58eRibD1--3xVXLJz9a4o_Xfnv3s",
    "authDomain": "hacking-for-gooooooood.firebaseapp.com",
    "databaseURL": "https://hacking-for-gooooooood.firebaseio.com/",
    "storageBucket": "hacking-for-gooooooood.appspot.com"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


storage.child("images/zebra.png").put("zebra.png")
url = storage.child("images/zebra.png").get_url(None)
print(url)
