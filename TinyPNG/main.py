import os
import tinify
tinify.key = "IAl6s3ekmONUVMEqWZdIp1nV2ItJLyPC"
FILE_SIZE_LIMIT = 1024 * 1024 # 1MB
def compress_file(file_path):
    """
    压缩单个文件，如果文件大小超过限制则进行压缩，否则跳过
    """
    file_size = os.path.getsize(file_path)
    if file_size > FILE_SIZE_LIMIT:
        print("Compressing file:", file_path)
        try:
            source = tinify.from_file(file_path)
            source.to_file(file_path)
            print("Compression successful:", file_path)
        except tinify.errors.AccountError:
            print("Compression failed: API key is invalid.")
        except tinify.errors.ConnectionError:
            print("Compression failed: network connection error.")
        except Exception as e:
            print("Compression failed:", e)
    else:
        print("Skipping file:", file_path)
def compress_folder(folder_path):
    """
    递归压缩文件夹中的所有图片文件
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith((".jpg", ".jpeg", ".png")):
                compress_file(file_path)
if __name__ == "__main__":
    folder_path = "./images"
    compress_folder(folder_path)