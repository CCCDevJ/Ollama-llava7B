import requests
import json
import base64

# image file path
image_path = 'compo_8_b_cabezal_1000.jpg'

# Read image and encode to base64
with open(image_path, 'rb') as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

url = "http://localhost:11434/api/generate"
prompt = "what's in this picture?"
model = "llava:13b"
# model = "llava:34b"

payload = {
    "model": model,
    "prompt": prompt,
    "stream": False,
    "images": [image_base64]
}

# Send POST request
response = requests.post(url, data=json.dumps(payload))

# Print response
print(response.text)
