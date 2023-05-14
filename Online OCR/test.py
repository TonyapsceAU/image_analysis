import requests

# Send a POST request to the Flask API
url = 'http://9428-34-147-0-147.ngrok.io/ocr'
files = {'image': open(image_name, 'rb')}
response = requests.post(url, files=files)

# Get the extracted text
text = response.text
print(text)