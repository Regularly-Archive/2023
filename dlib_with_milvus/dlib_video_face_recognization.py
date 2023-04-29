import cv2 
import dlib
import logging
import dlib_face_recognization as fr
import datetime
import random
import asyncio
from pymilvus import connections, CollectionSchema, FieldSchema, DataType, Collection, utility
from myThread import MyThread
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

# 加载人脸数据库
fr.connect_milvus()
collection = Collection(fr.MILVUS_COLLECTION_NAME)
collection.load()

# 处理画面，特征对比方案
async def process(collection, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    faces = detector(gray, 1)

    if len(faces) != 0:
        for i in range(len(faces)):
            face = faces[i]
            shape = predictor(gray, face)
            face_descriptor = face_reco_model.compute_face_descriptor(gray, shape)
            x, y, w, h = face.left(), face.top(), face.right() - face.left(), face.bottom() - face.top()
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
            t1 = MyThread(fr.search_face, (collection, face_descriptor))
            t1.start()
            t1.join()
            # search_results = fr.search_face(collection, face_descriptor)
            search_results = t1.getResult()
            if search_results:
                person_dist = search_results[0][0].distance
                person_label = search_results[0][0].entity.get('person_name')
                frame = fr.cv2AddChineseText(frame , f'{str(person_label)},{str(round(person_dist, 4))}', (x + 5, y - 35),(255, 0, 0), 30)
            else:
                frame = fr.cv2AddChineseText(frame , f'Unknow', (x + 5, y - 35),(255, 0, 0), 30) 
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            rand = random.randint(1111, 9999)
            cv2.imwrite(f'./output/Capture-{timestamp}-{rand}.jpg', frame) 

    return frame

async def main():
    video = cv2.VideoCapture('286370351.mp4')
    # video = cv2.VideoCapture(0)
    fps = video.get(cv2.CAP_PROP_FPS)

    while video.isOpened():
        ret, frame = video.read()
        if frame is None: 
            break
        
        frame = await process(collection, frame)
        cv2.imshow("Face Recognization", frame)
        
        if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
            break 

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())