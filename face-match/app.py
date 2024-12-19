from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import dlib
import numpy as np
import os, io, uuid
from PIL import Image
from utils import (
    compute_features_of_face,
    save_faatures_to_database,
    search_images_from_database,
    update_face_label,
    query_face_data,
    delete_face_data
)

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

@app.post("/faces/upload")
async def upload_image(label: str, image: UploadFile = File(...)):
    file_content, file_extention, image_array = await process_image(image)

    features = compute_features_of_face(face_model, image_array)
    if features is None:
        return {
            "code": 500,
            "error": "No face detected in the image."
        }
    
    faceUrl, faceId = save_image_and_get_id(file_content, file_extention, features, label)
    
    return {
        "code": 200,
        "data": {
            "faceId": str(faceId),
            "faceUrl": faceUrl,
            "faceLabel": label,
         }
    }

@app.post("/faces/search")
async def search_image(top: int = 5, threshold: float = 0.25, image: UploadFile = File(...)):
    file_content, file_extention, image_array = await process_image(image)

    features = compute_features_of_face(face_model, image_array)
    if features is None:
        return {
            "code": 500,
            "error": "No face detected in the image."
        }
    
    faceUrl = save_image(file_content, file_extention)

    input = {
      "faceUrl": faceUrl
    }

    search_results = search_images_from_database(features, top , threshold)

    return {
        "code": 200,
        "data": {
            "input": input,
            "output": search_results,
        }
    }



@app.get("/faces")
async def get_faces(label: str = None, page: int = 1, pageSize: int = 10):
    total, rows = query_face_data(label=label, page=page, page_size=pageSize)
    return {
        "code": 200,
        "data": {
            'total': total,
            'rows': rows,
        }
    }

@app.delete("/faces/{face_id}")
async def remove_face(face_id: str):
    try:
        delete_face_data(face_id)
        return {
            "code": 200,
            "message": "Face data deleted successfully."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.put("/faces/{face_id}")
async def update_face(face_id, label):
    try:
        flag = update_face_label(face_id, label)
        return {
            "code": 200,
            "message": "Face data deleted successfully."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def process_image(image: UploadFile):
    file_content = await image.read()
    file_extention = os.path.splitext(image.filename)[1]
    image = Image.open(io.BytesIO(file_content))
    image_array = np.asarray(image)
    return file_content, file_extention, image_array

def save_image(file_content, file_extention):
    fileName = str(uuid.uuid1()).replace("-", "")
    filePath = f'./statics/{fileName}{file_extention}'
    with open(filePath, 'wb') as fw:
        fw.write(file_content)
    return f'/statics/{fileName}{file_extention}'

def save_image_and_get_id(file_content, file_extention, features, label):
    faceUrl = save_image(file_content, file_extention)
    faceId = save_faatures_to_database(features, label, faceUrl)
    return faceUrl, faceId

def process_search_results(search_results, threshold):
    output = []
    if search_results:
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
    return output
    