from google.cloud import storage
from PIL import Image

# Enable Storage
client = storage.Client()

# Reference an existing bucket.
bucket = client.get_bucket('hacking-for-gooooooood.appspot.com')

# Upload a local file to a new file to be created in your bucket.
zebraBlob = bucket.blob('zebra')
zebraBlob.upload_from_filename(filename='zebra')

# Download a file from your bucket.
#giraffeBlob = bucket.get_blob('giraffe.jpg')
#giraffeBlob.download_as_string()
