# Send to single device.
from pyfcm import FCMNotification

push_service = FCMNotification(api_key="AAAAXcxEn-s:APA91bFNEwRE8zcelyBM8dhbQ1hDPkWXFyK2zN5vnVigp3YRZvOilJJasmCAKmYpDEjbWE4_PF2ZbNBNzy51ppCXKo90NDUrgGYnWAHvnglqXNsjtEXDOBs2bEotcOelZ8f1h_IvFDyy")

# OR initialize with proxies

#proxy_dict = {
#    "http"  : "http://127.0.0.1",
#        "https" : "http://127.0.0.1",
#    }
#push_service = FCMNotification(api_key="AAAAXcxEn-s:APA91bFNEwRE8zcelyBM8dhbQ1hDPkWXFyK2zN5vnVigp3YRZvOilJJasmCAKmYpDEjbWE4_PF2ZbNBNzy51ppCXKo90NDUrgGYnWAHvnglqXNsjtEXDOBs2bEotcOelZ8f1h_IvFDyy", proxy_dict=proxy_dict)

# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

registration_id = "fMXYRHTn9D8:APA91bFY1VgkqkDWo39QHoEP2PzgCj3auDElvWuftnXiAyMp3cNfgER6Rq2dMLy1J4oWpV2o7vdtdKZoSC_RkmmWMW1F_XdHmUYFFBsz6vjAekA-zweh0-kRMJJBHjht0pvIPoiawyQ4"
message_title = "VIA SPOTTED!"
message_body = "Lynn was seen at your front door"
result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

# Send to multiple devices by passing a list of ids.
#registration_ids = ["<device registration_id 1>", "<device registration_id 2>", ...]
#message_title = "Uber update"
#message_body = "Hope you're having fun this weekend, don't forget to check today's news"
#result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)

print result
