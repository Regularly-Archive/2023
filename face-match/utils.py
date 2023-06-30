import dlib
import cv2
import numpy as np
import uuid
from pymilvus import connections, CollectionSchema, FieldSchema, DataType, Collection, utility

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

def save_faatures_to_database(features, label, url, collection_name="face_match"):
    connections.connect(alias="default", user='minioadmin',password='minioadmin',host='localhost', port='19530')
    collection = None
    if not utility.has_collection(collection_name):
       collection = create_milvus_collection(collection_name)
       create_milvus_index(collection, 'face_features')
    else:
       collection = Collection(collection_name)
    
    data = [
        [label],
        [url],
        [np.array(features)],
    ]
    mr = collection.insert(data)
    collection.flush()
    return mr.primary_keys[0]

def create_milvus_collection(collection_name):
    face_id = FieldSchema(
        name="face_id", 
        dtype=DataType.INT64, 
        auto_id=True,
        is_primary=True, 
    )
    face_label = FieldSchema(
        name="face_label", 
        dtype=DataType.VARCHAR, 
        max_length=200,
    )
    face_url = FieldSchema(
        name="face_url", 
        dtype=DataType.VARCHAR, 
        max_length=200,
    )
    face_features = FieldSchema(
        name="face_features", 
        dtype=DataType.FLOAT_VECTOR, 
        dim=128
    )
    schema = CollectionSchema(
        fields=[face_id, face_label, face_url, face_features], 
        description="a face features dababase based on milvus"
    )
    return Collection(name=collection_name, schema=schema, using='default', shards_num=2)

def create_milvus_index(collection, fieldName):
    index_params = { "metric_type":"L2", "index_type":"FLAT", "params":{ } }
    collection.create_index(field_name=fieldName, index_params=index_params)

def search_images_from_database(features, limit=5, collection_name="face_match"):
    connections.connect(alias="default", user='minioadmin',password='minioadmin',host='localhost', port='19530')
    collection = Collection(collection_name)
    collection.load()
    
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    
    return collection.search(
        data=[np.array(features).tolist()],
        anns_field="face_features", 
        param=search_params,
        limit=limit, 
        expr=None,
        output_fields=['face_id','face_label','face_url'],
        consistency_level="Strong"
    )