import os, shutil
from dlib_face_recognization import FACES_DIR

for file in os.listdir(FACES_DIR):
    file_path = os.path.join(FACES_DIR, file)
    file_ext = os.path.splitext(file_path)[1]
    if file_ext in ['.jpg','.png','.jpeg']:
        folder_name = os.path.splitext(file)[0]
        folder_path = os.path.join(FACES_DIR, folder_name)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        
        shutil.move(file_path, os.path.join(folder_path, file))
