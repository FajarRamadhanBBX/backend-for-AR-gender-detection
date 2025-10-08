from fastapi import FastAPI, HTTPException
import numpy as np
import uvicorn
from pydantic import BaseModel
import io
import base64
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model

app = FastAPI()

class ImageRequest(BaseModel):
    image: str

MODEL_PATH = "model.h5"
INPUT_WIDTH = 64
INPUT_HEIGHT = 64

try:
    model = load_model(MODEL_PATH)
    print("Load model berhasil")
except Exception as e:
    print("Load model gagal", e)
    model = None

def preprocess_image(image_bytes):
    img = Image.open(image_bytes).convert("RGB")
    img = img.resize((INPUT_WIDTH, INPUT_HEIGHT))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.get("/")
async def root():
    print("home")
    return {"message": "API is running"}

@app.post("/predict")
async def predict(req: ImageRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model tidak berhasil dimuat")
    
    try:
        image_bytes = base64.b64decode(req.image)
        processed_image = preprocess_image(io.BytesIO(image_bytes))
        prediction = model.predict(processed_image)
        
        prob_perempuan, prob_laki = float(prediction[0][0]), float(prediction[0][1])

        if prob_laki > prob_perempuan:
            gender = "pria"
            confidence_score = prob_laki
        else:
            gender = "wanita"
            confidence_score = prob_perempuan

        return {
            "full_result": prediction.tolist(),
            "prediction": gender,
            "confidence": confidence_score
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error saat memproses gambar: {str(e)}")

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
