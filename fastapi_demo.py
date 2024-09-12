from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import requests
import json
import base64
import os

app = FastAPI()

# Directory to save uploaded images
upload_dir = "uploaded_images"
os.makedirs(upload_dir, exist_ok=True)
model = "llava:13b"
# model = "llava:34b"


@app.post("/process_image")
async def process_image(prompt: str = Form(...), file: UploadFile = File(...)):
    try:
        # Save the uploaded image locally
        # file_location = os.path.join(upload_dir, file.filename)
        # with open(file_location, "wb") as f:
        #     f.write(file.file.read())
        #
        # # Read the image and encode it to base64
        # with open(file_location, "rb") as image_file:
        #     image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

        # Check if prompt or file is missing
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")
        if not file:
            raise HTTPException(status_code=400, detail="File is required")

        # Read the uploaded image and encode it to base64
        image_base64 = base64.b64encode(await file.read()).decode("utf-8")

        # Prepare the payload for the external API request
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "images": [image_base64]
        }

        # Send the POST request to the external API
        response = requests.post(url, data=json.dumps(payload))

        # Check if the request was successful
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error from external API")

        # Return the response from the external API
        return JSONResponse(content=response.json())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Function to start the FastAPI application
def start_app():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    start_app()
