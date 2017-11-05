Easy Lock
=======

Easy Lock is a facial recognition door lock that gives the owner the ability to control their front door remotely and powerfully.

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

#### Add button

The add buttons open the camera and allow the user to take a picture of a new face to register them to be recognized by the camera.

#### Person struct

The Person struct defines a single contact stored in the application. Information contained in the person struct includes the URL corresponding to the person's image, the saved name, the timestamp, and a key to upload to the database.

``` swift

struct Person {
    var mediaURL: String?
    var name: String?
    var timestamp: Date?
    var firebaseKey: String
}

```

#### Table

The table displays a scrollable list of the Person objects representing real-life people who have permission to open the door. 

### Shine Tab

Google Cloud Functions
---------------

Google Cloud Functions take the input from the camera and send the image, along with the matched name, to the Amazon SNS service to be published.

Amazon SNS
---------------

Amazon SNS stands for Amazon Simple Notification Service and is powered by Amazon Web Services. It provides half of the functionality of the PubSub structure of our application and handles the publishing of information to be retrieved by the Lambda function.

#### Topics

Easy Lock is registered as a topic under the Amazon SNS account so that information published to this topic can be accepted by the subscribers to this topic.

#### Subscriptions

Subscriptions manage the "subscribers" that are authorized to receive the published information. Here, the SNS will be publishing the name of the face at the door as well as the URL corresponding to the image in the Firebase database so that it can be displayed to the user.


Amazon Lambda Function
---------------

The AWS Lambda function is a subscriber to the SNS and will take the output of the SNS service and upload it to AlgoliaSearch to be displayed in the mobile app and searchable.

#### lambda_handler

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


Python Facial Recognition
---------------

The facial recognition technology scans the image displayed by the front door every 5 frames and uses machine learning modules to compare the image to the known faces stored by the user.


Firebase Storage
---------------

Firebase is a basic database with real-time synchronization to store the contacts and the images corresponding to the faces at the front door.



