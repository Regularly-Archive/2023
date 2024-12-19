import os
import dlib
import cv2
import numpy as np
import uuid
from pymilvus import connections, CollectionSchema, FieldSchema, DataType, Collection, utility
from config import MILVUS_CONFIG, SQLITE_DB_PATH, DATABASE_URL
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3  

Base = declarative_base()

class FaceData(Base):
    __tablename__ = 'face_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String, nullable=False)
    url = Column(String, nullable=False)
    face_id = Column(String, nullable=False)


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_to_sqlite(label, url, face_id):
    db = next(get_db())
    new_face_data = FaceData(label=label, url=url, face_id=face_id)
    db.add(new_face_data)
    db.commit()
    db.refresh(new_face_data)
    return new_face_data.id

def query_face_data(label=None, page=1, page_size=10):
    db = next(get_db())
    query = db.query(FaceData)
    
    if label:
        query = query.filter(FaceData.label.like(f"%{label}%"))
    
    total_count = query.count()
    
    results = query.offset((page - 1) * page_size).limit(page_size).all()
    return total_count, list(map(lambda x: { 'id': x.id, 'faceLabel':x.label, 'faceUrl':x.url, 'faceId':x.face_id }, results))

def delete_face_data(face_id):
    db = next(get_db())
    record = db.query(FaceData).filter(FaceData.face_id == face_id).first()
    
    if record:
        url = record.url
        
        db.delete(record)
        db.commit()
        
        connections.connect(alias="default", user=MILVUS_CONFIG["user"], password=MILVUS_CONFIG["password"], host=MILVUS_CONFIG["host"], port=MILVUS_CONFIG["port"])
        collection = Collection(MILVUS_CONFIG["collection_name"])
        collection.delete(expr=f"face_id in [{int(face_id)}]")
        
        if os.path.exists(url):
            os.remove(url)

def compute_features_of_face(face_model, image):
    face_detector = dlib.get_frontal_face_detector()
    faces = face_detector(image, 1)
    if len(faces) == 0:
        return None
    face = faces[0]
    shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    shape = shape_predictor(image, face)
    features = face_model.compute_face_descriptor(image, shape)
    return features

def save_faatures_to_database(features, label, url, collection_name=MILVUS_CONFIG["collection_name"]):
    connections.connect(alias="default", user=MILVUS_CONFIG["user"], password=MILVUS_CONFIG["password"], host=MILVUS_CONFIG["host"], port=MILVUS_CONFIG["port"])
    collection = None
    if not utility.has_collection(collection_name):
       collection = create_milvus_collection(collection_name)
       create_milvus_index(collection, 'face_features')
    else:
       collection = Collection(collection_name)
    
    data = [
        [np.array(features)],
    ]
    mr = collection.insert(data)
    collection.flush()

    save_to_sqlite(label, url, str(mr.primary_keys[0]))
    
    return mr.primary_keys[0]

def create_milvus_collection(collection_name):
    face_id = FieldSchema(
        name="face_id", 
        dtype=DataType.INT64, 
        auto_id=True,
        is_primary=True, 
    )
    face_features = FieldSchema(
        name="face_features", 
        dtype=DataType.FLOAT_VECTOR, 
        dim=128
    )
    schema = CollectionSchema(
        fields=[face_id, face_features], 
        description="a face features dababase based on milvus"
    )
    return Collection(name=collection_name, schema=schema, using='default', shards_num=2)

def create_milvus_index(collection, fieldName):
    index_params = { "metric_type":"L2", "index_type":"FLAT", "params":{ } }
    collection.create_index(field_name=fieldName, index_params=index_params)

def search_images_from_database(features, limit=5, threshold=0.25):
    # 连接到 Milvus
    connections.connect(alias="default", user=MILVUS_CONFIG["user"], password=MILVUS_CONFIG["password"], host=MILVUS_CONFIG["host"], port=MILVUS_CONFIG["port"])
    collection = Collection(MILVUS_CONFIG["collection_name"])
    collection.load()
    
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

    search_results = collection.search(
        data=[np.array(features).tolist()],
        anns_field="face_features", 
        param=search_params,
        limit=limit, 
        expr=None,
        output_fields=['face_id'],
        consistency_level="Strong"
    )
    
    face_ids = []
    distances = []
    for result in search_results[0]:
        face_ids.append(str(result.entity.get('face_id')))
        distances.append(result.distance)
    
    db = next(get_db())
    records = db.query(FaceData).filter(FaceData.face_id.in_(face_ids)).all()
    
    record_dict = {record.face_id: record for record in records}
    
    output = []
    for face_id, distance in zip(face_ids, distances):
        if distance <= threshold:
            record = record_dict.get(str(face_id))
            if record:
                output.append({
                    "faceId": record.face_id,
                    "faceLabel": record.label,
                    "faceUrl": record.url,
                    "distance": distance 
                })
    
    return output

def update_face_label(face_id, new_label):
    db = next(get_db())
    record = db.query(FaceData).filter(FaceData.face_id == face_id).first()
    
    if record:
        record.label = new_label 
        db.commit()
        return True 
    return False