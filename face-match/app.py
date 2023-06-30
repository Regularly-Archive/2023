from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import dlib
import numpy as np
import os, io, uuid
from PIL import Image
from utils import compute_features_of_face, save_faatures_to_database, search_images_from_database

app = FastAPI()
app.mount("/statics", StaticFiles(directory="statics"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


face_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

@app.post("/upload")
async def upload_image(label: str, image: UploadFile = File(...)):
    file_content = await image.read()
    file_extention = os.path.splitext(image.filename)[1]
    image = Image.open(io.BytesIO(file_content))
    image = np.asarray(image)

    features = compute_features_of_face(face_model, image)
    if features is None:
        return {
            "code": 500,
            "error": "No face detected in the image."
        }
    
    fileName = str(uuid.uuid1()).replace("-","")
    filePath = f'./statics/{fileName}{file_extention}'
    with open(filePath, 'wb') as fw:
        fw.write(file_content)

    faceUrl = f'/statics/{fileName}{file_extention}'
    faceId = save_faatures_to_database(features, label, faceUrl)
    

    return {
        "code": 200,
        "data": {
            "faceId": str(faceId),
            "faceUrl": faceUrl,
            "faceLabel": label,
         }
    }


@app.post("/search")
async def search_image(top: int = 5, threshold: float = 0.25, image: UploadFile = File(...)):
    file_content = await image.read()
    file_extention = os.path.splitext(image.filename)[1]
    image = Image.open(io.BytesIO(file_content))
    image = np.asarray(image)

    features = compute_features_of_face(face_model, image)
    if features is None:
        return {
            "code": 500,
            "error": "No face detected in the image."
        }
    
    fileName = str(uuid.uuid1()).replace("-","")
    filePath = f'./statics/{fileName}{file_extention}'
    with open(filePath, 'wb') as fw:
        fw.write(file_content)

    faceUrl = f'/statics/{fileName}{file_extention}'

    input = {
      "faceUrl": faceUrl
    }

    search_results = search_images_from_database(features, top)
    if search_results:
        output = []
        for item in search_results[0]:
            if item.distance > threshold:
                continue

            result = {
                "distance": str(item.distance),
                "faceId": str(item.entity.get('face_id')),
                "faceLabel": item.entity.get('face_label'),
                "faceUrl": item.entity.get('face_url')
            }
            output.append(result)

        return {
            "code": 200,
            "data": {
                "input": input,
                "output": output,
            }
        }
    else:
        return {
            "code": 200,
            "data": {
                "input": input,
                "output": [],
            }
        }
    