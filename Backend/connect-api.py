from fastapi import FastAPI, UploadFile
from typing import List
from pydantic import BaseModel
from tensorflow import keras, stack
from tensorflow.io import decode_image
from tensorflow.image import resize
import time

app = FastAPI()
# pre-load the model so everything is just faster.
model = keras.models.load_model("./models/BEST-cnn.keras")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")    # defining the root directory
async def root():
    return {"message": "hello world manya"}

name1 = "SIH 2023"
@app.get("/greet/{name}")
async def name(name: str = name1):
    return {"message": f"welcome to {name}"}

@app.get("/health")    # just to check if the api is working
def check_health():
    return {"status": "API is working!!"}

# main project logic -------->
class ImageInput(BaseModel):
    images: List[UploadFile]
    pincode: str

# make a little function here to postprocess the model's output
# LABEL and FORMAT tensors correctly :)
def proprocess(pred):
    pass

@app.post("/predict/")
async def predict_images(request: ImageInput):
    processed_images = []
    starttime = time.time()
    for img in request.images:
        # Read the JSON image data
        json_image_data = await img.read()
        # Decode the image from JSON data, and resize
        image_tensor = decode_image(json_image_data, channels=3)  # Set the number of color channels (3 for RGB)
        resized_image = resize(image_tensor, target_size=(256, 256))
        # Append the processed image to the list
        processed_images.append(resized_image)

    # Convert the list of processed images to a TensorFlow tensor
    images_tensor = stack(processed_images)

    # get prediction from the model
    prediction = model.predict(images_tensor)
    endtime = time.time()
    ttime = endtime - starttime
    # replace this with a more elaborate argmax function
    final_pred = prediction.numpy().tolist()
    
    return {"prediction" : final_pred, 'exectime' : ttime}

if __name__ == '__main__':
    # CODE FOR SERVER
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)