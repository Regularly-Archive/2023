import os
import dlib
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import csv
import logging
import uuid, random
from pymilvus import connections, CollectionSchema, FieldSchema, DataType, Collection, utility

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Dlib 正向人脸检测器
detector = dlib.get_frontal_face_detector()

# Dlib 人脸特征点检测器
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')

# Dlib 人脸识别模型
face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

# 常量定义
FACES_DIR = './faces/'
FACES_FEATURES_CSV_FILE = './data/features_all.csv'
FACES_FATURES_DISTANCE_THRESHOLD = 0.4
OUTPUT_DIR = './output/'
MILVUS_COLLECTION_NAME = 'faces'

def get_mean_features_of_face(path):
    path = os.path.abspath(path)
    subDirs = [os.path.join(path, f) for f in os.listdir(path)]
    subDirs= list(filter(lambda x:os.path.isdir(x), subDirs))
    for index in range(0, len(subDirs)):
        subDir = subDirs[index]
        person_label = os.path.split(subDir)[-1]
        image_paths = [os.path.join(subDir, f) for f in os.listdir(subDir)]
        image_paths = list(filter(lambda x:os.path.isfile(x), image_paths))
        feature_list_of_person_x = []
        for image_path in image_paths:
            if os.path.split(image_path)[-1].split(".")[-1] != "jpg":
                continue
            
            # 计算每一个图片的特征
            feature = get_128d_features_of_face(image_path)
            if feature == 0:
                logger.warning(f"The image '{image_path}' can not extract face feature.")
                continue
            
            feature_list_of_person_x.append(feature)
            logger.info(f"Extracting face feature from image '{image_path}' finished.")
        
        # 计算当前人脸的平均特征
        features_mean_person_x = np.zeros(128, dtype=object, order='C')
        if feature_list_of_person_x:
            features_mean_person_x = np.array(feature_list_of_person_x, dtype=object).mean(axis=0)
        
        logger.info(f"Calculating face feature for person '{image_path}' finished.")
        yield (features_mean_person_x, person_label)

def get_128d_features_of_face(image_path):
    image = Image.open(image_path)
    image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    faces = detector(image, 1)

    if len(faces) != 0:
        shape = predictor(image, faces[0])
        face_descriptor = face_reco_model.compute_face_descriptor(image, shape)
    else:
        face_descriptor = 0
    return face_descriptor

def extract_features_to_milvus(faces_dir):
    collection = None
    if not utility.has_collection(MILVUS_COLLECTION_NAME):
        collection = create_collection(MILVUS_COLLECTION_NAME)
        create_index(collection, 'person_face')
    else:
        collection = Collection(MILVUS_COLLECTION_NAME)

    mean_features_list = list(get_mean_features_of_face(faces_dir))
    person_names = list(map(lambda x:x[1], mean_features_list))
    person_faces_1 = list(map(lambda x:x[0].tolist(), mean_features_list))
    person_faces_2 = [[random.random() for _ in range(128)] for _ in range(len(mean_features_list))]
    person_ids = [i+1 for i in range(len(mean_features_list))]
    mr = collection.insert([person_ids, person_names, person_faces_1])
    collection.flush()

def get_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    return np.sqrt(np.sum(np.square(feature_1 - feature_2)))

def compare_face_fatures_with_database(collection, image_path):
    image = Image.open(image_path)
    image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    faces = detector(image, 1)
    
    campare_results = []
    if len(faces) != 0:
        for i in range(len(faces)):
            face = faces[i]
            shape = predictor(image, faces[0])
            face_descriptor = face_reco_model.compute_face_descriptor(image, shape)
            x, y, w, h = face.left(), face.top(), face.right() - face.left(), face.bottom() - face.top()
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 1)
            
            search_results = search_face(collection, face_descriptor)
            if search_results:
                person_dist = search_results[0][0].distance
                person_label = search_results[0][0].entity.get('person_name')
                image = cv2AddChineseText(image , f'{str(person_label)},{str(round(person_dist, 4))}', (x + 5, y - 35),(255, 0, 0), 30)
                campare_results.append((person_label, person_dist))
        
        # 输出人脸比对结果
        output_image = os.path.split(image_path)[-1].split('.')[0] + '_Output.jpg'
        output_image = os.path.join(OUTPUT_DIR, output_image)
        cv2.imwrite(output_image, image)

    return campare_results

def cv2AddChineseText(img, text, position, textColor=(0, 255, 0), textSize=30):
    if (isinstance(img, np.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    draw = ImageDraw.Draw(img)
    fontStyle = ImageFont.truetype("simsun.ttc", textSize, encoding="utf-8")
    draw.text(position, text, textColor, font=fontStyle)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

def connect_milvus():
    connections.connect(
        alias="default", 
        user='minioadmin',
        password='minioadmin',
        host='localhost', 
        port='19530'
    )
    
def create_collection(collection_name='faces'):
    person_id = FieldSchema(
        name="person_id", 
        dtype=DataType.INT64, 
        is_primary=True, 
    )
    person_name = FieldSchema(
        name="person_name", 
        dtype=DataType.VARCHAR, 
        max_length=200,
    )
    person_face = FieldSchema(
        name="person_face", 
        dtype=DataType.FLOAT_VECTOR, 
        dim=128
    )
    schema = CollectionSchema(
        fields=[person_id, person_name, person_face], 
        description="testing face search with milvus"
    )
    return Collection(
        name=collection_name, 
        schema=schema, 
        using='default', 
        shards_num=2
    )

def create_index(collection, fieldName):
    index_params = {
        "metric_type":"IP", # LR:欧式距离, IP:内积
        "index_type":"FLAT",
        "params":{ }
    }
    collection.create_index(
        field_name=fieldName, 
        index_params=index_params
    )

def search_face(collection, feature):
    search_params = {"metric_type": "IP", "params": {"nprobe": 10}}
    
    return collection.search(
        data=[np.array(feature).tolist()],
        anns_field="person_face", 
        param=search_params,
        limit=20, 
        expr=None,
        output_fields=['person_id','person_name'],
        consistency_level="Strong"
    )

def main():
  
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    total_images = 0
    matched_images = 0

    collection = Collection(MILVUS_COLLECTION_NAME)
    collection.load()

    # 加载测试人脸数据
    faces_dir = os.path.abspath(FACES_DIR)
    subDirs = [os.path.join(faces_dir, f) for f in os.listdir(faces_dir)]
    subDirs = list(filter(lambda x:os.path.isdir(x), subDirs))
    for subDir in subDirs:
        image_paths = [os.path.join(subDir, f) for f in os.listdir(subDir)]
        image_paths = list(filter(lambda x:os.path.isfile(x), image_paths))
        total_images += len(image_paths)
        for image_path in image_paths:
            result = compare_face_fatures_with_database(collection, image_path)
            if len(result) == 0:
                logger.warning(f"The image '{image_path}' can not be detected.")
                continue

            sorted(result, key=lambda x:x[1])
            predict = result[0][0]
            actual = os.path.split(subDir)[-1]
            logger.info(f"Process image {image_path} finsihed. Predict：{predict}, Actual：{actual}，Distance：{result[0][1]}")
            if predict == actual:
                matched_images += 1

    logger.info(f'Correct Rate：{round(matched_images / total_images * 100, 4)}%')

if __name__ == '__main__':
    
    connect_milvus()
     
    utility.drop_collection(MILVUS_COLLECTION_NAME)

    if (not utility.has_collection(MILVUS_COLLECTION_NAME)) or Collection(MILVUS_COLLECTION_NAME).is_empty:
        extract_features_to_milvus(FACES_DIR)

    main()