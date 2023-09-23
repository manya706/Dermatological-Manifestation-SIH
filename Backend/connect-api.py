from fastapi import FastAPI, UploadFile, File
import uvicorn
from PIL import Image
from typing import List
from pydantic import BaseModel
from tensorflow import keras
import io

app = FastAPI()

@app.get("/")    # defining the root directory
async def root():
    return {"message": "hello world manya"}

name1 = "SIH 2023"
@app.get("/{name}")
async def name(name : str):
    return {"message": f"welcome to {name1}"}

@app.get("/health")    # just to check if the api is working
def check_health():
    return {"status": "API is working!!"}

# main project logic -------->

class ImageInput(BaseModel):
    images: List[UploadFile]

def load_image(file):
    image = Image.open(io.BytesIO(file.read()))
    return image

def preprocess_image(image, target_size=(256, 256)):
    resized = image.resize(target_size)
    return resized

@app.get("/predict")
async def predict(model, images):
    for i, image in enumerate(images):
        prediction = model.predict(images)
    
    


@app.post("/predict/")
def predict_images(images: ImageInput):
    processed_images = []
    for uploaded_image in images.images:
        image = load_image(uploaded_image)
        preprocessed_image = preprocess_image(image)
        processed_images.append(preprocessed_image)

    
    # model = load_model("models\BEST-cnn.keras")
    model = keras.models.load_model('models\cnn-20230923-050016 (Current Best).keras')

    # Predict using the model
    prediction = predict(model, processed_images)

    return {"prediction": prediction}