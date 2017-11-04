from pyfcm import FCMNotification   # send push notifications
import threading                    # run on background thread
import cv2                          # capture frames from webcam
import time                         # get current time
import firebase_helper


push_service = FCMNotification(api_key="AAAAXcxEn-s:APA91bFNEwRE8zcelyBM8dhbQ1hDPkWXFyK2zN5vnVigp3YRZvOilJJasmCAKmYpDEjbWE4_PF2ZbNBNzy51ppCXKo90NDUrgGYnWAHvnglqXNsjtEXDOBs2bEotcOelZ8f1h_IvFDyy")

last_sent_notifications = {}
notificationQueue = []

'''
    FUNCTION: sends a push notification to a single device (ie. <name> was seen as your front door)
'''
def send_FCM_Notification(name):
    registration_id = "fMXYRHTn9D8:APA91bFY1VgkqkDWo39QHoEP2PzgCj3auDElvWuftnXiAyMp3cNfgER6Rq2dMLy1J4oWpV2o7vdtdKZoSC_RkmmWMW1F_XdHmUYFFBsz6vjAekA-zweh0-kRMJJBHjht0pvIPoiawyQ4"
#    registration_id = "fiBDcSV80CQ:APA91bHI1diAIhIJfsrlVNo-sFjeafqy-C6a5S4gAe4gDMuCpB5_aOT0Ovh3HtxY8Xa4xKwwfdkh2xq0JlHBVEAY3rjzmBhpZYIGJ0sulrW635y_0jezulhXYujUWjvH2Ge0V1bbe7nQ"
    message_title = "ALERT"
    message_body = name + " was seen at your front door"
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
    last_sent_notifications[name] = time.time()
    print(result)


'''
    FUNCTION: determines if a notification should be sent, once every minute
'''
def should_send_notification(name):
    if name in last_sent_notifications and time.time() - last_sent_notifications[name] < 10:
        return False
    else:
        return True

'''
    FUNCTION: saves a frame from cv2 to the local disk
'''
def save_frame(filepath, frame):
    cv2.imwrite(filepath, frame)


class NotificationSender(threading.Thread):
   def __init__(self, threadID, ):
      threading.Thread.__init__(self)
      self.threadID = threadID
   def run(self):
      sendNotifications()

def sendNotifications():
    while True:
        while len(notificationQueue) > 0:
            notification = notificationQueue.pop()
            notification_frame = notification[0]
            notification_name = notification[1]
            notification_key = notification[2]
            save_frame("saved_frames/" + notification_key + ".jpg", notification_frame)
            firebase_helper.send_frame_to_database(notification_key, "saved_frames/" + notification_key + ".jpg", notification_name)
            send_FCM_Notification(notification_name)

notificationThread = NotificationSender("NotificationSender")
notificationThread.start()
