import threading
import time

class Thread_one(threading.Thread):
   def __init__(self, threadID, ):
      threading.Thread.__init__(self)
      self.threadID = threadID
   def run(self):
      print ("Starting " + self.name)
      time.sleep(2)
      print ("Exiting " + self.name)

class Thread_two(threading.Thread):
   def __init__(self, threadID, ):
      threading.Thread.__init__(self)
      self.threadID = threadID
   def run(self):
      print ("Starting " + self.name)
      time.sleep(4)
      print ("Exiting " + self.name)

thread1 = Thread_one("first thread")
thread1.start()

thread2 = Thread_two("second thread")
thread2.start()
