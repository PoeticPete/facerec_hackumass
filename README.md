Easy Lock
=======

Easy Lock is a facial recognition door lock that gives the owner the ability to control their front door remotely and powerfully.

Documentation is available at the following URL:
[http://hackumass-docs.s3-website-us-east-1.amazonaws.com/](http://hackumass-docs.s3-website-us-east-1.amazonaws.com/)

Mobile Application
---------------

The Mobile Application provides a User Interface to communicate with the backend. It allows the user to unlock or lock their door with the press of a button, examine and search a list of detected faces at their front door, and update the list of recognizable contacts.

### Key Tab

The key tab provides the user with a button in order to lock or unlock the door. The view will monitor whether the door is locked or unlocked and update accordingly to alert the user. 

``` objective-c

    @objc fileprivate func keyButtonTapped() {
        let info:[String:Any] = ["status": !isLocked,
                                 "lastChanged": [".sv": "timestamp"]]
        ref.child("doors").child("door1").updateChildValues(info)
    }


    fileprivate func observeDoor() {
        ref.child("doors").child("door1").child("status").observe(.value) { (snap) in
            if let locked = snap.value as? Int{
                if locked == 1 {
                    self.isLocked = true
                } else {
                    self.isLocked = false
                }
                self.keyButton.isEnabled = true
            }
        }
    }

```

### Monitor Tab

The monitor tab accepts images from the camera and displays them so that the user can scroll through to see if any faces were detected at their door. This tab is also searchable by name and timestamp so that the owner can limit the scope to a certain time period or individual.

``` swift

    func observeFrames() {
        ref.child("savedFrames").child("door1").queryOrdered(byChild: "timestamp").queryLimited(toLast: 1).observe(.childAdded) { (snap) in
            self.frameData.insert(FrameData(snapshot: snap), at: 0)
            
            self.lastFrameKey = String(snap.key.dropLast())
            
            self.tableView.reloadData()
        }
    }

```

### People Tab

The people tab lists the faces of the people who are registered to gain access through the door. 

###### Add button

The add buttons open the camera and allow the user to take a picture of a new face to register them to be recognized by the camera.

###### Person struct

The Person struct defines a single contact stored in the application. Information contained in the person struct includes the URL corresponding to the person's image, the saved name, the timestamp, and a key to upload to the database.

``` swift

struct Person {
    var mediaURL: String?
    var name: String?
    var timestamp: Date?
    var firebaseKey: String
}

```

###### People Table

The table displays a scrollable list of the Person objects representing real-life people who have permission to open the door. 

### Shine Tab

The Shine tab provides functionality and compatibility with the [Liberty Mutual Shine API](https://developers.solarialabs.com/). The Shine API provides a home safety score given coordinates or an address. This tab will give the owner a score from the Shine API and, based on the score, recommend settings for two- or three- factor authentication in order to unlock the door. Currently, this API is limited to the Boston Metro area. 

Google Cloud Functions
---------------

Google Cloud Functions listens for "create" events in Firebase and publishes the data to Amazon SNS. The data in this proof of concept project are the "savedFrames" for the purpose of monitoring. Amazon SNS then relays the data to the respective subscribers.

``` javascript

exports.publishFrame = functions.database.ref('/savedFrames/door1/{id}').onCreate(event => {
  var sns = new AWS.SNS();
  sns.publish({
      Message: JSON.stringify(event.data),
      TopicArn: '[Amazon Resource Number]'
  }, function(err, data) {
      if (err) {
          return;
      }
      const newData = event.data.val();
      return 1;
  });
});

```

Amazon SNS
---------------

Amazon SNS stands for Amazon Simple Notification Service and is powered by Amazon Web Services. It provides half of the functionality of the PubSub structure of our application and handles the publishing of information to be retrieved by the Lambda function.

### Topics

Easy Lock is registered as a topic under the Amazon SNS account so that information published to this topic can be accepted by the subscribers to this topic.

### Subscriptions

Subscriptions manage the "subscribers" that are authorized to receive the published information. Here, the SNS will be publishing the name of the face at the door as well as the URL corresponding to the image in the Firebase database so that it can be displayed to the user.


Amazon Lambda Function
---------------

The AWS Lambda function is a subscriber to the SNS and will take the output of the SNS service and upload it to AlgoliaSearch to be displayed in the mobile app and searchable.

### lambda_handler

The lambda_handler function is located inside of the algolia.py file. This function defines what happens when the Lambda function receives a notification from Amazon SNS. The function takes the String from SNS, converts it to JSON, processes the information, and adds it to the Algolia database. 

``` python
def lambda_handler(event, context):
    client = algoliasearch.Client([algoliaID], [algolia API key])
    index = client.init_index("easylock_savedFrames")
    modifiedEvent = json.loads(event['Records'][0]['Sns']['Message'])
    modifiedEvent["timestamp"] = int(modifiedEvent["timestamp"] / 1000)
    res = index.add_object(modifiedEvent)
```

Algolia Search
---------------

Algolia is a powerful search engine and database to store the pictures and contact names that have been detected by the front door. 

``` json

{
  "name": "Tyler",
  "photoURL": "[firebase photo URL]",
  "timestamp": 1509849033,
  "objectID": "755220"
}

```

Python Facial Recognition
---------------
The facial recognition technology scans the image displayed by the front door every 5 frames and uses machine learning modules to compare the image to the known faces stored by the user.


``` python

# start the camera stream on the main thread
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=1.0/scaling_factor, fy=1.0/scaling_factor)

    # Only process every  5th frame of video to save battery
    if counter % 12 == 0:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = list(face_recognition.face_distance(known_encodings, face_encoding))
            name = "Unknown"
            best_match_dist = 1
            for i in range(len(match)):
                if match[i] < best_match_dist and match[i] < .55:
                    best_match_dist = match[i]
                    name = names[i]

            face_names.append(name)
        counter = 0

    counter += 1
```

The python file, main.py, runs an infinite loop recording out of the webcam. Every fifth frame, the video is analyzed to find any faces present. If there are any faces detected, then the program will display a box in the image around the face. If this face has been matched with any others, then the box will be green. Otherwise, the box will be red.

``` python
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled
        top *= scaling_factor
        right *= scaling_factor
        bottom *= scaling_factor
        left *= scaling_factor

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), -1)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)
```

The program determines the "distance" between the face in the image and each face in the database. If the distance is below a certain threshold, then there is a match. The threshold has been put at 0.55 because empirical results show this to be the most consistent value. Consistency is based on the number of false positives and false negatives.

Firebase Storage
---------------

Firebase is a basic database with real-time synchronization to store the contacts and the images corresponding to the faces at the front door.



